"""
LB Computer Help - Browser Agent v3.6
======================================
Interface to Browser Use for Facebook automation.

v3.6 CHANGES (Feb 10, 2026):
- Text entry: JS ClipboardEvent paste (replaces native input which typed \\n literally)
- Single JS call inserts entire post with proper newlines
- Posts complete in 7-8 steps instead of 15+
- API mode: Real Browser Use Cloud API integration for autonomous VPS operation

v3.5 CHANGES (Feb 6, 2026 PM):
- Post button: Find SPAN with 'Post' text → .closest('[role="button"]') → click
- max_steps: 18 (v3.6 typically completes in 7-8)

STILL REQUIRED:
- All Facebook URLs MUST include ?_fb_noscript=1
- Space+Backspace "wiggle" after text entry for React state reconciliation
- NEVER use Escape key - it closes Facebook modals
- "LB Computer Help" triggers mention dropdown - dismiss by clicking modal header
"""

import json
import logging
import os
import time
import requests
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Facebook noscript parameter - REQUIRED for reliable loading in Browser Use
FB_NOSCRIPT = "?_fb_noscript=1"

# Browser Use Cloud API
BROWSER_USE_API_BASE = "https://api.browser-use.com/api/v2"


def _ensure_noscript_url(url: str) -> str:
    """Ensure Facebook URL has the ?_fb_noscript=1 parameter."""
    if not url:
        return url
    url = url.rstrip('/')
    if '?_fb_noscript=1' in url:
        return url
    if '?' in url:
        return url + '&_fb_noscript=1'
    return url + '/?_fb_noscript=1'


def _ensure_trailing_slash(url: str) -> str:
    """Ensure URL has trailing slash for path appending."""
    if not url.endswith('/'):
        return url + '/'
    return url


def _escape_js_string(text: str) -> str:
    """Escape text for safe embedding in a JS string literal."""
    return (text
            .replace('\\', '\\\\')
            .replace('"', '\\"')
            .replace("'", "\\'")
            .replace('\n', '\\n')
            .replace('\r', ''))


@dataclass
class PostResult:
    """Result of a posting attempt."""
    success: bool
    message: str
    task_id: Optional[str] = None
    screenshot_path: Optional[str] = None
    error: Optional[str] = None


class BrowserAgent:
    """
    Agent for executing Facebook posting via Browser Use.

    Supports two modes:
    - 'mcp': Direct MCP tool calls (used when running from Claude Code)
    - 'api': HTTP API calls to Browser Use cloud (used on VPS/cron)
    """

    def __init__(self, profile_id: str, mode: str = 'mcp',
                 dry_run: bool = True, api_key: Optional[str] = None):
        self.profile_id = profile_id
        self.mode = mode
        self.dry_run = dry_run
        self.api_key = api_key or os.environ.get('BROWSER_USE_API_KEY', '')

    # ========================================
    # API Client Methods (for autonomous mode)
    # ========================================

    def _api_headers(self) -> Dict:
        """Get headers for Browser Use API calls."""
        return {
            "X-Browser-Use-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    def _api_create_session(self) -> str:
        """Create a Browser Use session with the configured profile."""
        resp = requests.post(
            f"{BROWSER_USE_API_BASE}/sessions",
            headers=self._api_headers(),
            json={"profileId": self.profile_id},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        session_id = data.get("id") or data.get("sessionId")
        logger.info(f"Created session: {session_id}")
        return session_id

    def _api_create_task(self, task: str, max_steps: int = 18,
                         session_id: Optional[str] = None) -> Dict:
        """Create a Browser Use task."""
        payload = {
            "task": task,
            "maxSteps": max_steps,
        }
        if session_id:
            payload["sessionId"] = session_id

        resp = requests.post(
            f"{BROWSER_USE_API_BASE}/tasks",
            headers=self._api_headers(),
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        logger.info(f"Created task: {data.get('id', 'unknown')}")
        return data

    def _api_poll_task(self, task_id: str, timeout: int = 600,
                       poll_interval: int = 10) -> Dict:
        """Poll a Browser Use task until completion or timeout."""
        start = time.time()
        while time.time() - start < timeout:
            try:
                resp = requests.get(
                    f"{BROWSER_USE_API_BASE}/tasks/{task_id}",
                    headers=self._api_headers(),
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                status = data.get("status", "unknown")

                if status in ("completed", "finished", "done"):
                    logger.info(f"Task {task_id} completed successfully")
                    return data
                elif status in ("failed", "error", "stopped"):
                    logger.error(f"Task {task_id} failed: {data.get('error', 'unknown')}")
                    return data
                else:
                    logger.debug(f"Task {task_id} status: {status} "
                                 f"(elapsed: {int(time.time() - start)}s)")
            except requests.RequestException as e:
                logger.warning(f"Poll error for {task_id}: {e}")

            time.sleep(poll_interval)

        logger.error(f"Task {task_id} timed out after {timeout}s")
        return {"status": "timeout", "id": task_id}

    # ========================================
    # Task Prompt Builders
    # ========================================

    def _build_post_task(self, payload: Dict) -> str:
        """
        Build the natural language task for Browser Use.

        v3.6 approach (Feb 10, 2026):
        1. Navigation with ?_fb_noscript=1
        2. Pre-engagement (scroll + like)
        3. Modal initialization with render verification
        4. Text entry via JS ClipboardEvent paste (entire post in one call)
        5. Dismiss mention dropdown + space/backspace wiggle
        6. Post submission via .closest('[role="button"]') JS from SPAN
        7. Post-submission verification
        """
        if not payload or 'group_url' not in payload or 'text' not in payload:
            raise ValueError("Payload must contain 'group_url' and 'text'")

        group_url = payload['group_url']
        group_url_noscript = _ensure_noscript_url(group_url)
        text = payload['text']
        text_js = _escape_js_string(text)

        # Determine if this is a Business Page or Group
        is_page = payload.get('is_page', False)
        write_prompt = '"Create a post" or "Create post"' if is_page else '"Write something..."'

        # Build the ClipboardEvent paste JS
        paste_js = (
            '(function(){'
            ' var editor = document.querySelector(\'div[role="dialog"] div[contenteditable="true"][role="textbox"]\');'
            ' if(!editor) editor = document.querySelector(\'div[contenteditable="true"][role="textbox"]\');'
            ' if(!editor) return \'NO_EDITOR\';'
            ' editor.focus();'
            f' var text = "{text_js}";'
            ' var dt = new DataTransfer();'
            " dt.setData('text/plain', text);"
            " var pe = new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true});"
            ' editor.dispatchEvent(pe);'
            " return 'PASTED';"
            '})()'
        )

        # Post button JS
        post_button_js = (
            "(function(){"
            "var spans=document.querySelectorAll('span');"
            "for(var i=spans.length-1;i>=0;i--){"
            "if(spans[i].textContent.trim()==='Post'&&spans[i].offsetWidth>0){"
            "var btn=spans[i].closest('[role=\"button\"]');"
            "if(btn&&btn.getAttribute('aria-disabled')!=='true'){"
            "btn.click();return 'BUTTON_CLICKED';}"
            "if(btn){return 'BUTTON_DISABLED';}"
            "spans[i].click();return 'SPAN_CLICKED';}}"
            "return 'NOT_FOUND';})()"
        )

        task = f"""You are a Facebook group posting bot. Follow these phases EXACTLY:

PHASE 1 - NAVIGATE:
Go to {group_url_noscript}
Wait for the page to fully load. If stuck on splash screen, try navigating to https://www.facebook.com first, wait for it to load, then navigate back to the group URL.

PHASE 2 - PRE-ENGAGE:
Scroll down 1-2 pages, like one post if possible, wait 3 seconds, scroll back to top.

PHASE 3 - OPEN POST EDITOR:
Click {write_prompt} to open the post modal. Wait 3 seconds for modal to render.

PHASE 4 - ENTER TEXT:
Click inside the editor to focus it, then run this JavaScript to paste text:
{paste_js}

PHASE 5 - DISMISS MENTION DROPDOWN + REACT WIGGLE:
"LB Computer Help" triggers a mention dropdown. Click the "Create post" modal header text to dismiss it. Then press Space followed by Backspace to activate React state.

PHASE 6 - SUBMIT:
Run this JavaScript to click the Post button:
{post_button_js}
Wait 5 seconds after clicking.

PHASE 7 - CONFIRM:
Verify the modal is gone and the post appears in the feed. Report success or failure.

FINAL REPORT - Report one of:
- SUCCESS_PENDING: Post submitted but pending admin approval
- SUCCESS_PUBLISHED: Post visible in feed
- SUCCESS_MODAL_CLOSED: Modal closed (assumed success)
- FAILED_MODAL_LOAD: Post editor never loaded
- FAILED_TEXT_ENTRY: Text could not be entered
- FAILED_POST_CLICK: Post button click had no effect
- FAILED_NOT_MEMBER: Not a member of this group
- FAILED_BLOCKED: Facebook security check encountered
- FAILED_OTHER: Any other failure (describe)"""

        return task.strip()

    # ========================================
    # Execution Methods
    # ========================================

    def execute_post(self, payload: Dict) -> PostResult:
        """
        Execute a Facebook post.

        In dry_run mode, just logs what would happen.
        """
        task = self._build_post_task(payload)

        if self.dry_run:
            logger.info(f"[DRY RUN] Would post to: {payload['group_name']}")
            logger.info(f"[DRY RUN] Content ID: {payload['post_id']}")
            logger.info(f"[DRY RUN] Photo: {payload.get('photo_filename', 'None')}")
            logger.info(f"[DRY RUN] Text preview: {payload['text'][:100]}...")
            logger.debug(f"[DRY RUN] Full task:\n{task}")

            return PostResult(
                success=True,
                message=f"[DRY RUN] Would post '{payload['post_id']}' to '{payload['group_name']}'"
            )

        if self.mode == 'mcp':
            return self._execute_mcp(task, payload)
        else:
            return self._execute_api(task, payload)

    def _execute_mcp(self, task: str, payload: Dict) -> PostResult:
        """
        Execute via MCP (when running from Claude Code).

        Returns the task details for Claude to execute via browser_task tool.
        """
        logger.info("MCP mode: Generating task for Claude execution")

        return PostResult(
            success=True,
            message="MCP task generated",
            error=json.dumps({
                'task': task,
                'profile_id': self.profile_id,
                'max_steps': 18,
                'group_name': payload.get('group_name', 'Unknown'),
            })
        )

    def _execute_api(self, task: str, payload: Dict) -> PostResult:
        """
        Execute via Browser Use Cloud API.

        For VPS/cron deployment. Creates a session, runs the task,
        polls for completion, and returns the result.
        """
        if not self.api_key:
            return PostResult(
                success=False,
                message="No API key configured",
                error="Set BROWSER_USE_API_KEY in .env or environment"
            )

        group_name = payload.get('group_name', 'Unknown')
        logger.info(f"API mode: Executing post to {group_name}")

        try:
            # Step 1: Create session with profile
            session_id = self._api_create_session()

            # Step 2: Create task
            task_data = self._api_create_task(
                task=task,
                max_steps=18,
                session_id=session_id,
            )
            task_id = task_data.get("id") or task_data.get("task_id")

            if not task_id:
                return PostResult(
                    success=False,
                    message=f"Failed to create task for {group_name}",
                    error=f"No task_id in response: {task_data}"
                )

            logger.info(f"Task {task_id} created for {group_name}, polling...")

            # Step 3: Poll for completion (10 min timeout)
            result = self._api_poll_task(task_id, timeout=600)
            status = result.get("status", "unknown")

            # Step 4: Interpret result
            task_output = result.get("output") or result.get("task_output") or ""
            is_success = result.get("is_success", False)

            if status in ("completed", "finished", "done") or is_success:
                # Check if the output indicates actual posting success
                success_indicators = [
                    "SUCCESS", "BUTTON_CLICKED", "published",
                    "posted", "visible in feed", "modal closed"
                ]
                post_success = any(
                    ind.lower() in str(task_output).lower()
                    for ind in success_indicators
                )

                return PostResult(
                    success=post_success,
                    message=f"{'SUCCESS' if post_success else 'COMPLETED_BUT_UNCERTAIN'}: {group_name}",
                    task_id=task_id,
                    error=None if post_success else f"Output: {task_output[:500]}"
                )
            else:
                return PostResult(
                    success=False,
                    message=f"FAILED: {group_name} (status: {status})",
                    task_id=task_id,
                    error=f"Status: {status}, Output: {str(task_output)[:500]}"
                )

        except requests.RequestException as e:
            logger.error(f"API request failed for {group_name}: {e}")
            return PostResult(
                success=False,
                message=f"API error for {group_name}",
                error=str(e)
            )
        except Exception as e:
            logger.error(f"Unexpected error for {group_name}: {e}")
            return PostResult(
                success=False,
                message=f"Error posting to {group_name}",
                error=str(e)
            )

    def monitor_group(self, group_url: str, group_name: str) -> PostResult:
        """Monitor a group for posting opportunities."""
        keywords = ["computer", "laptop", "slow", "broken", "help", "IT", "tech"]
        keywords_str = ", ".join(f'"{k}"' for k in keywords)
        group_url_noscript = _ensure_noscript_url(group_url)

        task = f"""
Navigate to {group_url_noscript}
Wait for the page to fully load.
Use the group's search function to search for any of these keywords: {keywords_str}
Look at posts from the past 24-48 hours.
For each relevant post where someone is asking for tech help:
- Note the poster's name
- Summarize what they need help with
- Note approximately how old the post is
Return a summary of opportunities found.
""".strip()

        if self.dry_run:
            logger.info(f"[DRY RUN] Would monitor: {group_name}")
            return PostResult(
                success=True,
                message=f"[DRY RUN] Would monitor '{group_name}' for opportunities"
            )

        if self.mode == 'mcp':
            return PostResult(
                success=True,
                message="MCP monitor task generated",
                error=json.dumps({
                    'task': task,
                    'profile_id': self.profile_id,
                    'max_steps': 15,
                    'group_name': group_name,
                })
            )
        else:
            return self._execute_api(task, {'group_name': group_name})


def generate_mcp_command(payload: Dict, profile_id: str) -> Dict:
    """
    Generate the Browser Use MCP command for use in Claude Code.

    Returns a dict that can be passed to the browser_task MCP tool.
    """
    agent = BrowserAgent(profile_id, mode='mcp', dry_run=False)
    task = agent._build_post_task(payload)

    max_steps = 18
    if payload.get('first_comment'):
        max_steps += 5

    return {
        'task': task,
        'profile_id': profile_id,
        'max_steps': max_steps,
    }


if __name__ == "__main__":
    # Test the browser agent
    logging.basicConfig(level=logging.DEBUG)

    agent = BrowserAgent(
        profile_id="0ab23467-abfc-45a1-b98d-1b199d6168cc",
        mode='mcp',
        dry_run=True
    )

    test_payload = {
        'group_id': 'test_group',
        'group_name': 'Test Group',
        'group_url': 'https://facebook.com/groups/test',
        'post_id': 'test_post_1',
        'text': 'This is a test post!\n\nHello world!',
        'photo_path': '/path/to/photo.jpg',
        'photo_filename': 'photo.jpg',
    }

    result = agent.execute_post(test_payload)
    print(f"\nResult: {result}")
