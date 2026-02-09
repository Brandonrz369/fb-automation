"""
LB Computer Help - Browser Agent v3.5
======================================
Interface to Browser Use MCP for Facebook automation.

v3.5 CHANGES (Feb 6, 2026 PM):
- Text entry: Native Browser Use `input` action (execCommand BROKEN as of Feb 6 PM)
- Post button: Find SPAN with 'Post' text → .closest('[role="button"]') → click
  The Post button is NOT a div element - all div[role="button"] selectors fail.
- max_steps reduced to 15 (v3.5 typically completes in 9)

STILL REQUIRED:
- All Facebook URLs MUST include ?_fb_noscript=1
- Space+Backspace "wiggle" after text entry for React state reconciliation
- NEVER use Escape key - it closes Facebook modals
"""

import base64
import json
import logging
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Facebook noscript parameter - REQUIRED for reliable loading in Browser Use
FB_NOSCRIPT = "?_fb_noscript=1"


def _ensure_noscript_url(url: str) -> str:
    """Ensure Facebook URL has the ?_fb_noscript=1 parameter."""
    if not url:
        return url
    # Strip trailing slash for clean append
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


def _text_to_b64(text: str) -> str:
    """Encode text to Base64 for safe JS transport. Eliminates all escaping issues."""
    return base64.b64encode(text.encode('utf-8')).decode('ascii')


@dataclass
class PostResult:
    """Result of a posting attempt."""
    success: bool
    message: str
    screenshot_path: Optional[str] = None
    error: Optional[str] = None


class BrowserAgent:
    """
    Agent for executing Facebook posting via Browser Use.

    Supports two modes:
    - 'mcp': Direct MCP tool calls (used when running from Claude Code)
    - 'api': HTTP API calls to Browser Use cloud (used on VPS)
    """

    def __init__(self, profile_id: str, mode: str = 'mcp', dry_run: bool = True):
        self.profile_id = profile_id
        self.mode = mode
        self.dry_run = dry_run

    def _build_post_task(self, payload: Dict) -> str:
        """
        Build the natural language task for Browser Use.

        v3.5 approach (Feb 6, 2026 PM):
        1. Navigation with ?_fb_noscript=1
        2. Pre-engagement (scroll + like)
        3. Modal initialization with render verification
        4. Text entry via native Browser Use `input` action + space/backspace wiggle
        5. Post submission via .closest('[role="button"]') JS from SPAN
        6. Post-submission verification
        """
        if not payload or 'group_url' not in payload or 'text' not in payload:
            raise ValueError("Payload must contain 'group_url' and 'text'")

        group_url = payload['group_url']
        group_url_noscript = _ensure_noscript_url(group_url)
        text = payload['text']
        photo_path = payload.get('photo_path')
        capture_rules = payload.get('capture_rules', False)

        # Build rules-capture step
        rules_step = ""
        if capture_rules:
            about_url = _ensure_noscript_url(
                _ensure_trailing_slash(group_url) + 'about'
            )
            rules_step = f"""PHASE 0 - CAPTURE GROUP RULES:
Navigate to {about_url}
Wait for the page to load completely.
Look for and record ALL of the following:
- "Group rules" section (numbered rules)
- Any mentions of allowed posting days
- Whether admin approval is required for posts
- Whether business/promotional posts are allowed or restricted
- Any posting frequency limits
- Any special restrictions or requirements

After recording rules, proceed to Phase 1.

"""

        # Build photo upload step
        photo_step = ""
        if photo_path:
            photo_step = """
OPTIONAL - PHOTO UPLOAD:
Look for a photo/image button in the post creation modal. Click it.
If a file picker appears, try to upload the image.
If upload fails or is not possible, proceed with text only - do NOT abort the post.

"""

        # Build first-comment step with pending-post awareness
        first_comment = payload.get('first_comment', '')
        comment_step = ""
        if first_comment:
            comment_b64 = _text_to_b64(first_comment)
            comment_step = f"""
PHASE 6 - FIRST COMMENT (only if post is visible, NOT pending):
If the post shows "pending admin approval", SKIP this phase entirely.
If the post is visible in the feed:
1. Navigate to {group_url_noscript} (reload the page)
2. Find your post (look for text "Just now" or "1 min" near your post content)
3. Click the "Comment" area on YOUR post
4. Wait 2 seconds for the comment box to be focused
5. Type the comment text using the input action:
{first_comment}
6. Press Enter or click the comment submit button
7. Verify the comment appears

If you cannot find your post or commenting fails, report it but still count the POST as successful.
"""

        # The main task prompt - v3.5 approach
        task = f"""{rules_step}PHASE 1 - NAVIGATION:
Navigate to {group_url_noscript}
IMPORTANT: The URL MUST contain ?_fb_noscript=1 - this is required for the page to load.
Wait for the page to fully load. You should see the group name and a "Write something..." area.
If the page shows only a Facebook logo/splash screen after 10 seconds, try refreshing.

PRE-CHECKS before proceeding:
- Can you see "Write something..." or a post creation area? If NO, check if you need to "Join Group" first - if so, ABORT and report "Not a member".
- Close any popup modals (cookie consent, notifications, etc.) that may be blocking the view.

PHASE 2 - PRE-ENGAGEMENT (humanize the session):
Scroll down the group feed slowly for about 10-15 seconds.
Find a recent post from another member and click the Like (thumbs up) reaction on it.
Wait 2 seconds, then scroll back to the top of the page.

PHASE 3 - OPEN POST EDITOR:
Click on the "Write something..." or "Create a public post..." input area.
Wait 3 seconds for the post creation modal to FULLY render.

CRITICAL VERIFICATION: The modal must show a text input area (NOT shimmering/loading placeholders).
- If you see shimmer/loading bars inside the modal, wait up to 10 more seconds.
- If the modal is STILL showing loading placeholders after 15 seconds total, close the modal, navigate to {group_url_noscript} again, and retry from Phase 3.
- If it fails a second time, ABORT and report "Modal failed to load".

PHASE 4 - ENTER TEXT:
Click on the text editor area inside the modal to focus it.
Wait 1 second for focus.

STEP 4A - TYPE TEXT using the native input action:
Type the following text into the editor (use the input action, NOT JavaScript):

{text}

STEP 4B - REACT STATE ACTIVATION (required after typing):
Wait 1 second after typing completes.
Then type a single SPACE character.
Then IMMEDIATELY type a single BACKSPACE character.
This "wiggle" forces React to reconcile its state with the actual DOM content.
The space+backspace leaves NO extra characters in the text.

STEP 4C - VERIFY text is visible in the editor and the Post button appears active (not grayed out).
If the Post button is still disabled after the wiggle, click the editor area again and try typing one more space then backspace.
{photo_step}
PHASE 5 - SUBMIT POST:
DO NOT press Escape - it will close the modal! If a dropdown menu or mention suggestion is covering the Post button, click somewhere else in the modal to dismiss it first.

Click the Post button using this JavaScript (finds the Post SPAN and traverses up to the clickable button):
(function(){{var spans=document.querySelectorAll('span');for(var i=spans.length-1;i>=0;i--){{if(spans[i].textContent.trim()==='Post'&&spans[i].offsetWidth>0){{var btn=spans[i].closest('[role="button"]');if(btn&&btn.getAttribute('aria-disabled')!=='true'){{btn.click();return 'BUTTON_CLICKED';}}if(btn){{return 'BUTTON_DISABLED';}}spans[i].click();return 'SPAN_CLICKED';}}}}return 'NOT_FOUND';}})()

Check the result:
- BUTTON_CLICKED = Success, proceed to verification
- BUTTON_DISABLED = Post button is disabled, text may not have registered. Go back to Step 4B and try the wiggle again, then retry this JS.
- SPAN_CLICKED = Fallback click on span directly, may or may not work. Wait and check.
- NOT_FOUND = Post button not found. Try clicking the Post button directly by visual position as fallback.

Wait 5 seconds after clicking.

VERIFICATION - Check for ONE of these success indicators:
a) A "Posting" spinner appeared and the modal closed = SUCCESS
b) A message saying "pending" or "awaiting admin approval" = SUCCESS (post submitted, waiting for mod review)
c) Your post text visible in the group feed = SUCCESS (post published)
d) The "Create post" modal disappeared and "Write something..." is visible again = LIKELY SUCCESS
e) The modal is still open with your text = FAILED (Post button click did not work)
f) An error message appeared = FAILED (report the error text)

{comment_step}
FINAL REPORT:
Report the outcome clearly:
- SUCCESS_PENDING: Post submitted but pending admin approval
- SUCCESS_PUBLISHED: Post visible in feed
- SUCCESS_MODAL_CLOSED: Modal closed (assumed success)
- FAILED_MODAL_LOAD: Post editor never loaded
- FAILED_TEXT_ENTRY: Text could not be entered / Post button stayed disabled
- FAILED_POST_CLICK: Post button click had no effect
- FAILED_NOT_MEMBER: Not a member of this group
- FAILED_BLOCKED: Facebook security check or posting block encountered
- FAILED_OTHER: Any other failure (describe what happened)"""

        return task.strip()

    def _build_monitor_task(self, group_url: str, keywords: list = None) -> str:
        """Build task to monitor a group for opportunities."""
        if keywords is None:
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
"""
        return task.strip()

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

        # Actual execution
        if self.mode == 'mcp':
            return self._execute_mcp(task, payload)
        else:
            return self._execute_api(task, payload)

    def _execute_mcp(self, task: str, payload: Dict) -> PostResult:
        """
        Execute via MCP (when running from Claude Code).

        Note: This returns the task details for Claude to execute,
        as MCP calls need to go through the Claude interface.
        """
        logger.info("MCP mode: Generating task for Claude execution")

        return PostResult(
            success=True,
            message="MCP task generated",
            error=json.dumps({
                'task': task,
                'profile_id': self.profile_id,
                'max_steps': 25,
                'group_name': payload.get('group_name', 'Unknown'),
            })
        )

    def _execute_api(self, task: str, payload: Dict) -> PostResult:
        """
        Execute via Browser Use Cloud API.

        For VPS deployment, this would make HTTP calls to Browser Use cloud.
        """
        try:
            logger.info(f"API mode: Would execute task for {payload.get('group_name', 'Unknown')}")
            return PostResult(
                success=True,
                message="API execution placeholder - implement with Browser Use SDK"
            )

        except Exception as e:
            logger.error(f"API execution failed: {e}")
            return PostResult(
                success=False,
                message="API execution failed",
                error=str(e)
            )

    def monitor_group(self, group_url: str, group_name: str) -> PostResult:
        """Monitor a group for posting opportunities."""
        task = self._build_monitor_task(group_url)

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

    # Calculate steps: base(15) + comment(5) + rules_capture(8)
    # v3.5: 15 base steps is sufficient (typically completes in 9)
    max_steps = 15
    if payload.get('first_comment'):
        max_steps += 5
    if payload.get('capture_rules'):
        max_steps += 8

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
