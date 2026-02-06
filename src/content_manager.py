"""
LB Computer Help - Content Manager
===================================
Handles content selection, photo matching, and history tracking.
"""

import yaml
import json
import random
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

        # Load posting history
        self.history = self._load_history()

    def _load_yaml(self, filename: str) -> Any:
        """Load a YAML configuration file."""
        filepath = self.config_dir / filename
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    def _load_history(self) -> Dict:
        """Load posting history from JSON file."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_history(self):
        """Save posting history to JSON file."""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2, default=str)

    def get_active_groups(self, tier: Optional[int] = None) -> List[Dict]:
        """Get all active groups, optionally filtered by tier."""
        groups = [g for g in self.groups if g.get('active', False)]
        if tier:
            groups = [g for g in groups if g.get('tier') == tier]
        return groups

    def select_groups_for_today(self) -> List[Dict]:
        """
        Select groups to post to today based on tier rotation and history.
        Returns a randomized list of groups.
        """
        selected = []
        today = datetime.now().strftime("%Y-%m-%d")
        day_of_week = datetime.now().weekday()  # 0=Monday, 6=Sunday

        # Tier 1: Post to 1-2 high-volume groups daily
        tier1_groups = self.get_active_groups(tier=1)
        random.shuffle(tier1_groups)
        selected.extend(tier1_groups[:2])

        # Tier 2: Post to 1 niche group every other day
        if day_of_week in [0, 2, 4]:  # Mon, Wed, Fri
            tier2_groups = self.get_active_groups(tier=2)
            if tier2_groups:
                selected.append(random.choice(tier2_groups))

        # Tier 3: Rotate through local groups (1 per day)
        tier3_groups = self.get_active_groups(tier=3)
        if tier3_groups:
            # Use day of year to rotate through tier 3 groups
            day_of_year = datetime.now().timetuple().tm_yday
            tier3_index = day_of_year % len(tier3_groups)
            selected.append(tier3_groups[tier3_index])

        # Limit to max posts per day
        max_posts = self.settings['posting']['max_posts_per_day']
        return selected[:max_posts]

    def get_eligible_content(self, group: Dict) -> List[Dict]:
        """
        Get content that is eligible for posting to a specific group.
        Filters by:
        1. Content category matches group's content_tags
        2. Content hasn't been posted to this group before
        """
        group_id = group['id']
        group_tags = set(group.get('content_tags', []))

        # Get history for this group
        group_history = self.history.get(group_id, [])
        posted_content_ids = {h['post_id'] for h in group_history}

        eligible = []
        for post in self.content:
            # Check if content category matches group tags
            if post.get('category') not in group_tags:
                continue

            # Check if already posted to this group
            if post['id'] in posted_content_ids:
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

        # Select a soft CTA for the first comment
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
