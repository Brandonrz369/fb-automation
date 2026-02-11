"""
LB Computer Help - Content Manager
===================================
Handles content selection, photo matching, and history tracking.
"""

import yaml
import json
import os
import random
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

# Soft CTA scripts for first comments (rotated)
SOFT_CTAS = [
    "If you want more tips like this, I share them weekly in my OC Tech Help group. It's free and no spam, promise!",
    "I post scam alerts as soon as I see them hitting OC in my tech group. Stay protected!",
    "Got a tech question? I answer them for free. No appointment needed - just DM me!",
    "Need help with yours? I'm local in OC and do house calls. Just send me a message!",
    "More tips like this on my page - LB Computer Help. Happy to help anytime!",
]

class ContentManager:
    def __init__(self, config_dir: Path, data_dir: Path):
        self.config_dir = config_dir
        self.data_dir = data_dir
        self.history_file = data_dir / "history.json"

        # Load configurations
        self.settings = self._load_yaml("settings.yaml")
        self.groups = self._load_yaml("groups.yaml")
        self.content = self._load_yaml("content_calendar.yaml")
        self.photos = self._load_yaml("photos_manifest.yaml")

        # Load group rules (personal account)
        self.group_rules = self._load_yaml("group_rules_personal.yaml") or {}

        # Load bi-weekly posting schedule
        self.weekly_schedule = self._load_yaml("weekly_schedule.yaml") or {}

        # Build group lookup by id
        self._group_lookup = {g['id']: g for g in self.groups}

        # Load posting history
        self.history = self._load_history()

    def _load_yaml(self, filename: str) -> Any:
        """Load a YAML configuration file."""
        filepath = self.config_dir / filename
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    def _load_history(self) -> Dict:
        """Load posting history from JSON file. Falls back to backup if corrupted."""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                # Try backup
                backup = self.history_file.with_suffix('.json.bak')
                if backup.exists():
                    try:
                        with open(backup, 'r') as f:
                            return json.load(f)
                    except (json.JSONDecodeError, ValueError):
                        pass
                return {}
        return {}

    def _save_history(self):
        """Save posting history to JSON file using atomic write.
        Writes to temp file first, then renames to prevent corruption."""
        # Save backup
        backup_file = self.history_file.with_suffix('.json.bak')
        if self.history_file.exists():
            try:
                import shutil
                shutil.copy2(self.history_file, backup_file)
            except OSError:
                pass

        # Atomic write: write to temp file in same dir, then rename
        fd, tmp_path = tempfile.mkstemp(
            dir=self.history_file.parent, suffix='.tmp'
        )
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(self.history, f, indent=2, default=str)
            os.replace(tmp_path, self.history_file)
        except Exception:
            # Clean up temp file on failure
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    # Day name mapping for posting_rules.promo_days
    DAY_NAMES = {
        0: "monday", 1: "tuesday", 2: "wednesday",
        3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"
    }

    def get_active_groups(self, tier: Optional[int] = None) -> List[Dict]:
        """Get all active groups, optionally filtered by tier."""
        groups = [g for g in self.groups if g.get('active', False)]
        # Exclude Business Page entries
        groups = [g for g in groups if g.get('type') != 'page']
        if tier:
            groups = [g for g in groups if g.get('tier') == tier]
        return groups

    def _is_allowed_today(self, group: Dict) -> bool:
        """Check if a group allows posting today based on posting_rules.promo_days."""
        rules = group.get('posting_rules', {})
        if not rules:
            return True  # No rules = allowed any day

        promo_days = rules.get('promo_days', ['any'])
        if not promo_days or 'any' in promo_days:
            return True

        today_name = self.DAY_NAMES[datetime.now().weekday()]
        return today_name in promo_days

    def _check_frequency_limit(self, group: Dict) -> bool:
        """Check if posting to this group would violate its frequency limit.
        Returns True if posting is OK, False if too soon."""
        rules = group.get('posting_rules', {})
        max_freq = rules.get('max_frequency', '')

        if not max_freq:
            # Default: 14-day cooldown
            return self._days_since_last_post(group['id']) >= 14

        if '1 per week' in max_freq:
            return self._days_since_last_post(group['id']) >= 7
        elif '1 per day' in max_freq:
            return self._days_since_last_post(group['id']) >= 1

        # Default cooldown
        return self._days_since_last_post(group['id']) >= 14

    def _days_since_last_post(self, group_id: str) -> int:
        """Get the number of days since the last post to a group."""
        group_history = self.history.get(group_id, [])
        if not group_history:
            return 999  # Never posted

        last_post = max(group_history, key=lambda h: h['timestamp'])
        last_time = datetime.fromisoformat(last_post['timestamp'])
        return (datetime.now() - last_time).days

    def _get_current_week(self) -> str:
        """Determine if we're in Week A or Week B.
        Even ISO week = Week A, Odd ISO week = Week B."""
        iso_week = datetime.now().isocalendar()[1]
        return 'week_a' if iso_week % 2 == 0 else 'week_b'

    def select_groups_for_today(self) -> List[Dict]:
        """
        Select groups to post to today using the bi-weekly schedule.

        Uses weekly_schedule.yaml which assigns specific groups to specific days
        in a 14-day rotation (Week A / Week B). This ensures:
        - Day-restricted groups only appear on their allowed days
        - 1/week groups appear in both weeks
        - Even load distribution (~6 posts/day)
        - Every active group is covered within 14 days

        Falls back to frequency-limit checking as a safety net.
        Returns a list of group dicts (excludes Business Page).
        """
        today_name = self.DAY_NAMES[datetime.now().weekday()]
        current_week = self._get_current_week()

        # Get today's scheduled group IDs from the bi-weekly schedule
        week_schedule = self.weekly_schedule.get(current_week, {})
        today_group_ids = week_schedule.get(today_name, [])

        if not today_group_ids:
            return []

        # Resolve group IDs to full group dicts, with safety checks
        selected = []
        for gid in today_group_ids:
            group = self._group_lookup.get(gid)
            if not group:
                continue
            if not group.get('active', False):
                continue
            # Safety: still check frequency limit (prevents double-posting)
            if not self._check_frequency_limit(group):
                continue
            selected.append(group)

        # Limit to max posts per day
        max_posts = self.settings['posting']['max_posts_per_day']
        return selected[:max_posts]

    def select_page_for_today(self) -> Optional[Dict]:
        """
        Check if today is a Business Page posting day (Mon/Wed/Fri).
        Returns the page config dict if yes, None if no.
        """
        day_of_week = datetime.now().weekday()  # 0=Mon, 2=Wed, 4=Fri
        if day_of_week not in [0, 2, 4]:
            return None

        # Find the business page entry
        for g in self.groups:
            if g.get('type') == 'page' and g.get('active', False):
                return g
        return None

    def generate_page_post_payload(self, page: Dict) -> Optional[Dict]:
        """
        Generate a post payload for the Business Page.
        Selects content based on today's day of week (Mon=horror, Wed=scam/tip, Fri=bts).
        """
        day_of_week = datetime.now().weekday()
        day_map = {0: 'monday', 2: 'wednesday', 4: 'friday'}
        target_day = day_map.get(day_of_week)

        if not target_day:
            return None

        # Find page content matching today's schedule_day
        page_id = page['id']
        page_history = self.history.get(page_id, [])
        posted_ids = {h['post_id'] for h in page_history}

        eligible = []
        for post in self.content:
            if post.get('content_type') != 'page':
                continue
            if post.get('schedule_day') != target_day:
                continue
            if post['id'] in posted_ids:
                continue
            eligible.append(post)

        if not eligible:
            # All content for this day has been posted - reset by using oldest
            for post in self.content:
                if post.get('content_type') == 'page' and post.get('schedule_day') == target_day:
                    eligible.append(post)
            if not eligible:
                return None

        post = eligible[0]
        text = self.get_text_for_audience(post, 'page')

        photo = self.select_photo_for_post(post)
        photo_path = None
        if photo:
            base_path = self.settings['photos']['base_path']
            photo_path = f"{base_path}/{photo['filename']}"

        return {
            'group_id': page_id,
            'group_name': page['name'],
            'group_url': page['url'],
            'post_id': post['id'],
            'text': text,
            'photo_path': photo_path,
            'photo_filename': photo['filename'] if photo else None,
            'audience_segment': 'page',
            'category': post.get('category'),
            'is_page': True,
        }

    # Categories considered promotional (skip for no-promo groups)
    PROMO_CATEGORIES = {'promo', 'repairs', 'smart_home', 'data_recovery', 'network'}

    def get_eligible_content(self, group: Dict) -> List[Dict]:
        """
        Get content that is eligible for posting to a specific group.
        Filters by:
        1. Content category matches group's content_tags
        2. Content hasn't been posted to this group before
        3. Respects posting_rules.content_only restriction
        4. Skips promo categories for groups with promo_allowed: false
        5. Skips page content for group posts
        """
        group_id = group['id']
        group_tags = set(group.get('content_tags', []))

        # Get posting rules
        rules = group.get('posting_rules', {})
        promo_allowed = rules.get('promo_allowed', True)
        content_only = rules.get('content_only', None)

        # Get history for this group
        group_history = self.history.get(group_id, [])
        posted_content_ids = {h['post_id'] for h in group_history}

        eligible = []
        for post in self.content:
            # Skip page content for group posts
            if post.get('content_type') == 'page':
                continue

            # Check if content category matches group tags
            if post.get('category') not in group_tags:
                continue

            # Check if already posted to this group
            if post['id'] in posted_content_ids:
                continue

            # If content_only is set, restrict to that category
            if content_only and post.get('category') != content_only:
                continue

            # If promo not allowed, skip promotional categories
            if not promo_allowed and post.get('category') in self.PROMO_CATEGORIES:
                continue

            eligible.append(post)

        return eligible

    def select_content_for_group(self, group: Dict) -> Optional[Dict]:
        """
        Select the best content for a specific group.
        Returns None if no eligible content available.
        """
        eligible = self.get_eligible_content(group)

        if not eligible:
            return None

        # Prefer content in calendar order (lower day number first)
        eligible.sort(key=lambda x: x.get('day', 999))

        return eligible[0]

    def get_text_for_audience(self, post: Dict, audience_segment: str) -> str:
        """Get the appropriate text variation for the audience segment."""
        variations = post.get('variations', {})

        # Fall back to community if segment not found
        text = variations.get(audience_segment, variations.get('community', ''))

        return text.strip()

    def select_photo_for_post(self, post: Dict) -> Optional[Dict]:
        """
        Select an appropriate photo for a post.
        Uses suggested photos first, then falls back to category matching.
        Prefers photos with lower used_count for rotation.
        """
        category = post.get('category')
        suggested = post.get('suggested_photos', [])

        # First try suggested photos
        if suggested:
            for filename in suggested:
                for photo in self.photos:
                    if photo['filename'] == filename:
                        return photo

        # Fall back to category matching
        matching_photos = [
            p for p in self.photos
            if p.get('category') == category
        ]

        if not matching_photos:
            # Try related categories
            category_map = {
                'tips': [],  # Tips often don't need photos
                'security': [],
                'promo': ['brand'],
                'smart_home': ['network'],
                'data_recovery': ['repairs'],
            }
            related = category_map.get(category, [])
            for rel_cat in related:
                matching_photos.extend([
                    p for p in self.photos
                    if p.get('category') == rel_cat
                ])

        if not matching_photos:
            return None

        # Sort by used_count (ascending) and pick first
        matching_photos.sort(key=lambda x: x.get('used_count', 0))
        return matching_photos[0]

    def increment_photo_usage(self, filename: str):
        """Increment the usage count for a photo."""
        for photo in self.photos:
            if photo['filename'] == filename:
                photo['used_count'] = photo.get('used_count', 0) + 1
                break

        # Save updated manifest
        manifest_path = self.config_dir / "photos_manifest.yaml"
        with open(manifest_path, 'w') as f:
            yaml.dump(self.photos, f, default_flow_style=False)

    def record_post(self, group_id: str, post_id: str, success: bool = True):
        """Record a post in the history."""
        if group_id not in self.history:
            self.history[group_id] = []

        self.history[group_id].append({
            'post_id': post_id,
            'timestamp': datetime.now().isoformat(),
            'success': success
        })

        self._save_history()

    def generate_post_payload(self, group: Dict) -> Optional[Dict]:
        """
        Generate a complete post payload for a group.
        Returns None if no content available.
        Respects posting_rules: skips CTA comment for no-promo groups.
        """
        # Select content
        post = self.select_content_for_group(group)
        if not post:
            return None

        # Get text for audience
        audience = group.get('audience_segment', 'community')
        text = self.get_text_for_audience(post, audience)

        # Select photo (optional)
        photo = self.select_photo_for_post(post)
        photo_path = None
        if photo:
            base_path = self.settings['photos']['base_path']
            photo_path = f"{base_path}/{photo['filename']}"

        # Check posting rules for CTA decisions
        rules = group.get('posting_rules', {})
        promo_allowed = rules.get('promo_allowed', True)

        # Only add soft CTA comment if promo is allowed in this group
        first_comment = None
        if promo_allowed:
            first_comment = random.choice(SOFT_CTAS)

        # Check if we need to capture rules for this group
        group_id = group['id']
        rules_entry = self.group_rules.get(group_id, {})
        needs_rules = not rules_entry.get('rules_captured', False)

        return {
            'group_id': group_id,
            'group_name': group['name'],
            'group_url': group['url'],
            'post_id': post['id'],
            'text': text,
            'photo_path': photo_path,
            'photo_filename': photo['filename'] if photo else None,
            'audience_segment': audience,
            'category': post.get('category'),
            'first_comment': first_comment,
            'capture_rules': needs_rules,
        }

    def get_stats(self) -> Dict:
        """Get statistics about content and posting."""
        total_groups = len(self.groups)
        active_groups = len(self.get_active_groups())
        total_content = len(self.content)

        posts_today = 0
        posts_this_week = 0
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        for group_id, posts in self.history.items():
            # Skip metadata entries
            if group_id.startswith('_'):
                continue
            if not isinstance(posts, list):
                continue
            for post in posts:
                post_time = datetime.fromisoformat(post['timestamp'])
                if post_time.date() == now.date():
                    posts_today += 1
                if post_time > week_ago:
                    posts_this_week += 1

        return {
            'total_groups': total_groups,
            'active_groups': active_groups,
            'total_content_pieces': total_content,
            'posts_today': posts_today,
            'posts_this_week': posts_this_week,
        }


if __name__ == "__main__":
    # Quick test
    config_dir = Path(__file__).parent.parent / "config"
    data_dir = Path(__file__).parent.parent / "data"

    cm = ContentManager(config_dir, data_dir)

    print("=== Content Manager Test ===")
    print(f"\nStats: {cm.get_stats()}")

    print("\n=== Today's Groups ===")
    for group in cm.select_groups_for_today():
        print(f"- {group['name']} ({group['audience_segment']})")
        payload = cm.generate_post_payload(group)
        if payload:
            print(f"  Content: {payload['post_id']}")
            print(f"  Photo: {payload['photo_filename']}")
            print(f"  Text preview: {payload['text'][:100]}...")
        else:
            print("  No eligible content!")
