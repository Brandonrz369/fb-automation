# VPS Transfer Guide - LB Computer Help FB Automation
# ====================================================
# Created: February 10, 2026
# VPS: root@5.161.45.43 (Hetzner)
# Local: /home/brandon/fb-automation/
# VPS Target: /root/fb-automation/

## CURRENT STATUS (as of Feb 10, 2026)

### What's Working
- **v3.6 posting engine**: 25/25 successful posts (12/12 + 13/13)
- **Content system**: 19 posts x 3 variations = 57 total pieces
- **Rules enforcement**: All 72 groups scraped, rules applied to code
- **Business Page support**: Mon/Wed/Fri schedule with separate content

### What Changed Since Last VPS Sync
The VPS does NOT have fb-automation yet (only job_bot exists at /root/job_bot/).
This is a FRESH deployment.

---

## STEP 1: Push Changes to GitHub

All these files need to be committed and pushed:

### Modified files (git tracked):
- `config/groups.yaml` - Rules-based re-architecture (16 deactivated, posting_rules added)
- `config/content_calendar.yaml` - 19 content pieces + 6 page posts
- `config/settings.yaml` - Updated posting config
- `src/content_manager.py` - Rules enforcement (day restrictions, frequency limits, tips-only filtering)
- `src/browser_agent.py` - v3.6 ClipboardEvent paste + .closest() post button
- `src/main.py` - API mode + Business Page support
- `requirements.txt` - Dependencies
- `run.sh` - Cron runner script
- `JUMPSTART.md` - Session quickstart doc

### New files (untracked):
- `data/master_group_rules.json` - Compiled rules database (72 groups)
- `data/scraped_rules_batch1-3.json` - Raw scrape data
- `data/scraped_rules_batch4-6.json` - Raw scrape data
- `data/scraped_rules_batch7-9.json` - Raw scrape data
- `data/scraped_rules_batch10.json` - Raw scrape data

### Files that should NOT be transferred:
- `.env` (has credentials - recreate on VPS)
- `data/history.json` (local posting history - start fresh on VPS)
- `assets/` directories (photos - need to be copied separately)
- `__pycache__/` directories
- `marketplace-photos/` (local only)

---

## STEP 2: Clone on VPS

```bash
ssh root@5.161.45.43

# Clone the repo
cd /root
git clone https://github.com/Brandonrz369/fb-automation.git
cd fb-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
FB_EMAIL=brandonrzz1998@mail.com
FB_PASSWORD=&p0wer24fromYah
BROWSER_USE_PROFILE_ID=0ab23467-abfc-45a1-b98d-1b199d6168cc
BROWSER_USE_API_KEY=bu_dEY5iTg2e5QhW1cVQqu22EM2JDOo8mIo0zsomte34I8
VPS_HOST=5.161.45.43
EOF

# Create data directories
mkdir -p data/logs

# Initialize empty history
echo '{}' > data/history.json
```

---

## STEP 3: Copy Photos

Photos are stored locally at `/home/brandon/fb-automation/assets/real-photos/`.
They need to be copied to the VPS:

```bash
# From local machine:
scp -r /home/brandon/fb-automation/assets/real-photos/ root@5.161.45.43:/root/fb-automation/assets/real-photos/
```

Check `config/settings.yaml` for the `photos.base_path` value and update if needed
(currently set to `/home/brandon/fb-automation/assets/real-photos` - needs to change to
`/root/fb-automation/assets/real-photos` on VPS).

---

## STEP 4: Update VPS-Specific Paths

In `config/settings.yaml`, update:
```yaml
photos:
  base_path: "/root/fb-automation/assets/real-photos"
```

In `run.sh`, the `cd "$(dirname "$0")"` already handles path detection.

---

## STEP 5: Set Up Cron Jobs

```bash
# Set timezone to Pacific
timedatectl set-timezone America/Los_Angeles

# Edit crontab
crontab -e

# Add these lines:
# Daily group posting at 9 AM PT
0 9 * * * /root/fb-automation/run.sh >> /root/fb-automation/data/logs/cron.log 2>&1

# Business Page posts: Mon/Wed/Fri at 10 AM PT
0 10 * * 1,3,5 /root/fb-automation/run.sh --page-only >> /root/fb-automation/data/logs/cron.log 2>&1
```

---

## STEP 6: Test Run

```bash
cd /root/fb-automation
source venv/bin/activate

# Check status (no posting)
python3 src/main.py --status

# Dry run (preview what would post)
python3 src/main.py --api --dry-run

# Actual single group test
python3 src/main.py --api --post anything_oc
```

---

## ARCHITECTURE OVERVIEW

### File Structure
```
fb-automation/
├── .env                          # Credentials (NOT in git)
├── run.sh                        # Cron entry point
├── requirements.txt              # Python deps
├── JUMPSTART.md                  # Session quickstart
├── VPS_TRANSFER.md               # This document
├── config/
│   ├── settings.yaml             # Global settings
│   ├── groups.yaml               # 96 groups (73 active) with posting_rules
│   ├── content_calendar.yaml     # 19 group posts + 6 page posts
│   ├── photos_manifest.yaml      # Photo mapping and usage tracking
│   └── group_rules_personal.yaml # Legacy rules (being replaced by posting_rules)
├── src/
│   ├── main.py                   # Entry point (--api, --page-only, --dry-run, etc.)
│   ├── content_manager.py        # Content selection + rules enforcement
│   └── browser_agent.py          # Browser Use integration (v3.6)
├── data/
│   ├── history.json              # Posting history tracker
│   ├── master_group_rules.json   # Compiled rules from 10-batch scrape
│   ├── scraped_rules_batch*.json # Raw scraping results
│   └── logs/                     # Run logs
└── assets/
    └── real-photos/              # Post photos (not in git)
```

### Code Flow
1. `run.sh` → `main.py --api` → `ContentManager.select_groups_for_today()`
2. Content manager filters by: active, tier rotation, day restrictions, frequency limits
3. For each group: `generate_post_payload()` → matches content to group tags + audience
4. Browser agent posts via Browser Use Cloud API (ClipboardEvent paste + JS post button)
5. History recorded, next group selected

### Rules Enforcement (NEW - Feb 10, 2026)
- `posting_rules.promo_days` → `_is_allowed_today()` checks day-of-week
- `posting_rules.max_frequency` → `_check_frequency_limit()` checks history
- `posting_rules.content_only` → `get_eligible_content()` restricts categories
- `posting_rules.promo_allowed: false` → `generate_post_payload()` skips CTA comment
- Groups with `active: false` are completely skipped

### Key Settings (config/settings.yaml)
- `posting.max_posts_per_day: 5` (safe limit)
- `posting.dry_run: true` (CHANGE TO false for production)
- `posting.delays.min_between_posts: 65` (minutes)
- `posting.delays.max_between_posts: 140` (minutes)

---

## IMPORTANT NOTES

1. **dry_run is TRUE by default** - Change to false in settings.yaml when ready
2. **Browser Use API key** has a credit balance - check https://cloud.browser-use.com/dashboard
3. **Never post same text to multiple groups** - content_manager handles this automatically
4. **Max 13-15 posts/day** - tested safe limit (Feb 6 session, no CAPTCHA)
5. **14-day cooldown per group** by default (7 days for frequency-limited groups)
6. **Stop immediately** on any CAPTCHA or spam warning
7. **Links go in first comment only**, never in main post text
8. **Photos must be real** (not AI-generated) per research consensus

---

## REMAINING WORK (Pick up on VPS)

### High Priority
- [ ] Deploy to VPS (this guide)
- [ ] Test dry-run on VPS
- [ ] Post to remaining active Tier 2 groups
- [ ] Post to unposted Tier 3 groups

### Medium Priority
- [ ] URL scraping for 20 PENDING_URL groups in groups.yaml
- [ ] Business Page posting schedule (need page content finalized)
- [ ] Quality audit of recent posts

### Low Priority
- [ ] Marketplace listings (product-framed rewrites in MARKETPLACE_LISTINGS.md)
- [ ] Blog post strategy (needs user input)
- [ ] Dashboard improvements
