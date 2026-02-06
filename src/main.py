#!/usr/bin/env python3
"""
LB Computer Help - Facebook Automation Main Script
===================================================

Entry point for the Facebook posting automation system.

Usage:
    python main.py                  # Run daily posting cycle
    python main.py --dry-run        # Preview what would be posted
    python main.py --status         # Show current stats
    python main.py --generate       # Generate today's posts (for manual execution)
    python main.py --post GROUP_ID  # Post to specific group

For VPS deployment, run via cron:
    0 9 * * * /home/user/fb-automation/run.sh
"""

import argparse
import json
import logging
import random
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from content_manager import ContentManager
from browser_agent import BrowserAgent, generate_mcp_command

# Setup paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
LOG_DIR = DATA_DIR / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


def setup_logging(level: str = "INFO"):
    """Configure logging."""
    log_file = LOG_DIR / f"automation_{datetime.now().strftime('%Y-%m-%d')}.log"

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)


def check_pause_file(settings: dict) -> bool:
    """Check if automation is paused."""
    pause_file = DATA_DIR / settings['safety'].get('pause_file', 'paused.lock')
    if pause_file.exists():
        return True
    return False


def run_daily_cycle(cm: ContentManager, agent: BrowserAgent, logger: logging.Logger):
    """
    Run the daily posting cycle.

    Selects groups, generates content, and executes posts with random delays.
    """
    logger.info("=" * 50)
    logger.info("Starting daily posting cycle")
    logger.info("=" * 50)

    # Check if paused
    if check_pause_file(cm.settings):
        logger.warning("Automation is PAUSED (pause file exists). Exiting.")
        return

    # Get stats
    stats = cm.get_stats()
    logger.info(f"Current stats: {stats}")

    # Select groups for today
    groups = cm.select_groups_for_today()
    logger.info(f"Selected {len(groups)} groups for today")

    if not groups:
        logger.warning("No groups selected for today!")
        return

    # Process each group
    success_count = 0
    failure_count = 0

    for i, group in enumerate(groups):
        logger.info(f"\n--- Processing group {i+1}/{len(groups)}: {group['name']} ---")

        # Generate payload
        payload = cm.generate_post_payload(group)

        if not payload:
            logger.warning(f"No eligible content for {group['name']} - skipping")
            continue

        logger.info(f"Content: {payload['post_id']} ({payload['category']})")
        logger.info(f"Audience: {payload['audience_segment']}")
        logger.info(f"Photo: {payload.get('photo_filename', 'None')}")

        # Execute post
        result = agent.execute_post(payload)

        if result.success:
            logger.info(f"SUCCESS: {result.message}")
            success_count += 1

            # Record in history (only if not dry run)
            if not agent.dry_run:
                cm.record_post(group['id'], payload['post_id'], success=True)

                # Update photo usage
                if payload.get('photo_filename'):
                    cm.increment_photo_usage(payload['photo_filename'])
        else:
            logger.error(f"FAILED: {result.message}")
            logger.error(f"Error: {result.error}")
            failure_count += 1

            # Check for safety threshold
            if failure_count >= cm.settings['safety']['max_failures']:
                logger.critical("Max failures reached - creating pause file")
                pause_file = DATA_DIR / cm.settings['safety']['pause_file']
                pause_file.write_text(f"Paused at {datetime.now()} after {failure_count} failures")
                break

        # Random delay before next post (humanization)
        if i < len(groups) - 1:  # Don't delay after last post
            min_delay = cm.settings['posting']['min_delay_minutes'] * 60
            max_delay = cm.settings['posting']['max_delay_minutes'] * 60
            delay = random.randint(min_delay, max_delay)
            logger.info(f"Waiting {delay // 60} minutes before next post...")

            if not agent.dry_run:
                time.sleep(delay)

    # Summary
    logger.info("\n" + "=" * 50)
    logger.info(f"Daily cycle complete: {success_count} success, {failure_count} failed")
    logger.info("=" * 50)


def generate_posts_for_manual_execution(cm: ContentManager, logger: logging.Logger):
    """
    Generate posts for manual execution via Claude Code.

    Outputs MCP commands that can be copy-pasted into Claude.
    """
    logger.info("Generating posts for manual execution...")

    profile_id = cm.settings['browser_use']['profile_id']
    groups = cm.select_groups_for_today()

    print("\n" + "=" * 60)
    print("GENERATED POSTS FOR MANUAL EXECUTION")
    print("=" * 60)

    for i, group in enumerate(groups):
        payload = cm.generate_post_payload(group)

        if not payload:
            print(f"\n[{i+1}] {group['name']}: No eligible content")
            continue

        mcp_command = generate_mcp_command(payload, profile_id)

        print(f"\n{'=' * 60}")
        print(f"POST {i+1}: {group['name']}")
        print(f"Content ID: {payload['post_id']}")
        print(f"Category: {payload['category']}")
        print(f"Audience: {payload['audience_segment']}")
        print(f"Photo: {payload.get('photo_filename', 'None')}")
        print("-" * 40)
        print("Browser Use Task:")
        print("-" * 40)
        print(f"Profile ID: {mcp_command['profile_id']}")
        print(f"Max Steps: {mcp_command['max_steps']}")
        print(f"\nTask:\n{mcp_command['task']}")
        print("-" * 40)
        print("Text Preview:")
        print(payload['text'][:500])
        if len(payload['text']) > 500:
            print("... [truncated]")

    print("\n" + "=" * 60)
    print("Copy the task prompts above to execute via Browser Use")
    print("=" * 60)


def post_to_specific_group(cm: ContentManager, agent: BrowserAgent,
                          group_id: str, logger: logging.Logger):
    """Post to a specific group by ID."""
    # Find the group
    group = None
    for g in cm.groups:
        if g['id'] == group_id:
            group = g
            break

    if not group:
        logger.error(f"Group not found: {group_id}")
        return

    logger.info(f"Posting to specific group: {group['name']}")

    payload = cm.generate_post_payload(group)

    if not payload:
        logger.warning(f"No eligible content for {group['name']}")
        return

    result = agent.execute_post(payload)

    if result.success:
        logger.info(f"SUCCESS: {result.message}")
        if not agent.dry_run:
            cm.record_post(group['id'], payload['post_id'], success=True)
    else:
        logger.error(f"FAILED: {result.error}")


def show_status(cm: ContentManager, logger: logging.Logger):
    """Display current automation status."""
    stats = cm.get_stats()

    print("\n" + "=" * 50)
    print("LB COMPUTER HELP - AUTOMATION STATUS")
    print("=" * 50)

    print(f"\nGROUPS:")
    print(f"  Total configured: {stats['total_groups']}")
    print(f"  Active: {stats['active_groups']}")

    print(f"\nCONTENT:")
    print(f"  Total pieces: {stats['total_content_pieces']}")

    print(f"\nPOSTING ACTIVITY:")
    print(f"  Posts today: {stats['posts_today']}")
    print(f"  Posts this week: {stats['posts_this_week']}")

    print(f"\nSETTINGS:")
    print(f"  Dry run: {cm.settings['safety']['dry_run']}")
    print(f"  Posts per day: {cm.settings['posting']['min_posts_per_day']}-{cm.settings['posting']['max_posts_per_day']}")

    # Check pause status
    if check_pause_file(cm.settings):
        print(f"\n⚠️  AUTOMATION IS PAUSED")
        pause_file = DATA_DIR / cm.settings['safety']['pause_file']
        print(f"  Reason: {pause_file.read_text()}")
    else:
        print(f"\n✅ Automation is active")

    # Today's groups
    print(f"\nTODAY'S TARGET GROUPS:")
    for group in cm.select_groups_for_today():
        payload = cm.generate_post_payload(group)
        content_status = payload['post_id'] if payload else "No eligible content"
        print(f"  - {group['name']} ({group['audience_segment']})")
        print(f"    Content: {content_status}")

    print("\n" + "=" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="LB Computer Help - Facebook Automation"
    )
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview without actually posting')
    parser.add_argument('--status', action='store_true',
                       help='Show current automation status')
    parser.add_argument('--generate', action='store_true',
                       help='Generate posts for manual execution')
    parser.add_argument('--post', type=str, metavar='GROUP_ID',
                       help='Post to a specific group')
    parser.add_argument('--log-level', type=str, default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(args.log_level)

    # Initialize content manager
    cm = ContentManager(CONFIG_DIR, DATA_DIR)

    # Check for dry_run override from settings
    dry_run = args.dry_run or cm.settings['safety']['dry_run']

    # Initialize browser agent
    agent = BrowserAgent(
        profile_id=cm.settings['browser_use']['profile_id'],
        mode='mcp',
        dry_run=dry_run
    )

    # Execute requested action
    if args.status:
        show_status(cm, logger)
    elif args.generate:
        generate_posts_for_manual_execution(cm, logger)
    elif args.post:
        post_to_specific_group(cm, agent, args.post, logger)
    else:
        run_daily_cycle(cm, agent, logger)


if __name__ == "__main__":
    main()
