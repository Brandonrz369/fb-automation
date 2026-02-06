"""
LB Computer Help - Browser Agent
=================================
Interface to Browser Use MCP for Facebook automation.

This module provides two execution modes:
1. Direct MCP call (when running from Claude Code)
2. API call (when running standalone on VPS)
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


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
        """Build the natural language task for Browser Use."""
        group_url = payload['group_url']
        text = payload['text']
        photo_path = payload.get('photo_path')
        capture_rules = payload.get('capture_rules', False)

        # Escape quotes in text for the prompt
        text_escaped = text.replace('"', '\\"').replace('\n', '\\n')

        # Build rules-capture step (visit About page first if needed)
        rules_step = ""
        if capture_rules:
            rules_step = f"""STEP 0 - CAPTURE GROUP RULES:
First, navigate to {group_url}about (add "about" to the group URL).
Wait for the page to load.
Look for and record ALL of the following:
- "Group rules" section (numbered rules)
- Any mentions of allowed posting days (e.g. "Self-promo Saturday", "Business Wednesday")
- Whether admin approval is required for posts
- Whether business/promotional posts are allowed or restricted
- Any posting frequency limits (e.g. "1 post per week")
- Any special restrictions or requirements

Write all the rules you find to a file called "group_rules_output.txt" using this format:
GROUP: {payload.get('group_name', 'Unknown')}
URL: {group_url}
ADMIN_APPROVAL: [yes/no/unknown]
PROMO_ALLOWED: [yes/no/restricted/unknown]
PROMO_DAYS: [specific days or "any"]
POST_FREQUENCY: [stated limit or "not specified"]
RULES: [list all rules found, separated by semicolons]
NOTES: [any other relevant info]

After recording rules, navigate back to {group_url}

"""

        # Build photo upload step if needed
        photo_step = ""
        if photo_path:
            photo_step = f"""
Look for a button to add a photo/image. Click it.

Note: An image upload is needed from path: {photo_path}
(If image upload is not possible in this browser session, proceed without the image)

"""

        # Build first-comment step
        first_comment = payload.get('first_comment', '')
        comment_step = ""
        if first_comment:
            first_comment_escaped = first_comment.replace('"', '\\"').replace('\n', '\\n')
            comment_step = f"""
After the post is published and visible in the feed, find your new post.
Click the "Comment" area on your post and type:
"{first_comment_escaped}"
Press Enter or click the comment submit button to post the comment.

"""

        task = f"""{rules_step}Navigate to {group_url}

Wait for the page to load completely.

Scroll down the group feed slowly for about 15-20 seconds to simulate browsing.

Find a recent post from another member and click the Like (thumbs up) reaction on it.

Scroll back to the top of the page.

Find and click on the "Write something..." input area or the post creation box.

Type the following text exactly (including line breaks):
"{text_escaped}"
{photo_step}Click the "Post" button to publish.

Wait a few seconds and verify the post appears in the group feed.
{comment_step}Report success or any errors encountered."""
        return task.strip()

    def _build_monitor_task(self, group_url: str, keywords: list = None) -> str:
        """Build task to monitor a group for opportunities."""
        if keywords is None:
            keywords = ["computer", "laptop", "slow", "broken", "help", "IT", "tech"]

        keywords_str = ", ".join(f'"{k}"' for k in keywords)

        task = f"""
Navigate to {group_url}

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

        # In MCP mode, we return the task for Claude to execute
        # The actual execution happens in the orchestration layer
        return PostResult(
            success=True,
            message="MCP task generated",
            error=json.dumps({
                'task': task,
                'profile_id': self.profile_id,
                'max_steps': 15,
                'group_name': payload['group_name'],
            })
        )

    def _execute_api(self, task: str, payload: Dict) -> PostResult:
        """
        Execute via Browser Use Cloud API.

        For VPS deployment, this would make HTTP calls to Browser Use cloud.
        """
        try:
            # This is a placeholder for the actual API implementation
            # When deploying to VPS, you would use the Browser Use Python SDK
            # or make direct HTTP calls to the Browser Use cloud API

            logger.info(f"API mode: Would execute task for {payload['group_name']}")

            # Example of what the API call would look like:
            # from browser_use import BrowserUseCloud
            # client = BrowserUseCloud(api_key=os.environ['BROWSER_USE_API_KEY'])
            # result = await client.run_task(
            #     task=task,
            #     profile_id=self.profile_id,
            #     max_steps=15
            # )

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

        # Similar execution flow as posting
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
