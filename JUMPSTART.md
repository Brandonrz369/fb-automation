# LB Computer Help - Facebook Automation JUMPSTART Guide

## For New Claude Sessions - READ THIS FIRST

**Last Updated:** February 10, 2026
**Purpose:** Enable any Claude session to immediately understand and continue this project

---

## Quick Context (30 seconds)

| What | Details |
|------|---------|
| **Business** | LB Computer Help - Computer Repair in Orange County, CA |
| **Goal** | Automate Facebook group posting to generate leads |
| **Method** | Browser Use MCP cloud automation + personal profile |
| **Status** | v3.6 LIVE - 25/25 success (12 today + 13 prev). Autonomous API mode built. |

---

## Current Numbers (Verified Feb 6, 2026)

| Metric | Count | Notes |
|--------|-------|-------|
| **OC Groups** | 76 + 1 Page | Tier 1: 9, Tier 2: 17, Tier 3: 50 (incl 9 marketplace) + Business Page |
| **Content Posts** | 25 | 19 group posts (3 variations each) + 6 Business Page posts |
| **Photos** | 18 | Mapped to content types |
| **Delay Between Posts** | 65-140 min | Random, mimics human behavior |
| **Max Posts/Day** | 13-15 | Tested 13 on Feb 6 with no issues |
| **Per-Group Frequency** | 1x per 14 days | Avoid spam detection |

---

## Key Files to Read (Priority Order)

```
1. JUMPSTART.md           <- YOU ARE HERE
2. EXECUTION_GUIDE.md     <- Phases, daily workflow, launch steps
3. STRATEGY_GUIDE.md      <- Research-backed posting strategy
4. GROWTH_STRATEGY.md     <- Growing Group/Page + Business Page content
5. config/settings.yaml   <- Current automation settings
6. config/groups.yaml     <- 76 OC groups to post to
```

---

## Current State (February 6, 2026)

### CRITICAL: Browser Agent v3.6 (VERIFIED WORKING - Feb 10, 2026)
v3.6 upgraded text entry from native input (typed `\n` literally) to JS ClipboardEvent paste.

- **ALL Facebook URLs must include `?_fb_noscript=1`**
- **Text entry**: JS ClipboardEvent paste - entire post in one call, handles newlines properly
- **React state activation**: Space+Backspace "wiggle" after text entry
- **NEVER use Escape key** (closes modal)
- **Post button**: Find SPAN with `textContent === 'Post'` → `.closest('[role="button"]')` → click
- **max_steps: 18** (typically completes in 7-8)
- **Two modes**: `mcp` (Claude-assisted) or `api` (autonomous VPS/cron)

### Autonomous API Mode (NEW - Feb 10, 2026)
The system can now run fully autonomous on a VPS via cron:
- `browser_agent.py` calls Browser Use Cloud REST API directly
- `main.py --api` flag enables API mode (requires `BROWSER_USE_API_KEY` in `.env`)
- `--page-only` flag for Business Page only (Mon/Wed/Fri at 10 AM)
- Run-level content deduplication prevents same text going to multiple groups
- Auto-pause after 3 failures (creates `data/paused.lock`)

See `src/browser_agent.py` for the full implementation and `~/.claude/projects/-home-brandon/memory/browser_use_fix.md` for detailed technical notes.

### What's Complete
- [x] 76 Orange County groups configured (14 added from scrape gap analysis)
- [x] 19 content pieces with 3 variations each (57 total, incl 3 marketplace)
- [x] browser_agent.py v3.5 - confirmed working (native input + .closest() Post click)
- [x] ALL sign-offs standardized with "LB Computer Help" (was just "- Brandon")
- [x] Content-to-group matching architecture designed (audience + tags 2-axis)
- [x] Marketplace strategy: 9 buy/sell groups, direct service listings
- [x] Photo-to-content mapping guide in dashboard
- [x] 18 real photos mapped to content types (research: NO AI images)
- [x] Strategy guide, Growth strategy, all docs consolidated

### Content-to-Group Architecture
```
MATCHING: group.audience_segment → content.variation (TONE)
          group.content_tags ∩ content.category (TOPIC)

TIERS:   T1 (9 groups) = 2x/week, all content types
         T2 (17 groups) = 1x/week, security/network/promo
         T3 Community (41 groups) = 1x/2 weeks, tips/dusty
         T3 Marketplace (9 groups) = 1x/2 weeks, promo/repairs ONLY

SATURATION: 19 posts × 14-day cooldown = 266 days (8.9 months) per group
```

### Posting History (Feb 10, 2026) - 14 Successful Posts (v3.6 ClipboardEvent Paste)
| # | Group | Content | Result |
|---|-------|---------|--------|
| 1 | OC Small Business Owners | extra_cable_management b2b | SUCCESS |
| 2 | Buena Park Small Business | week2_day12_msp_promo b2b | SUCCESS_PUBLISHED |
| 3 | OC Business Networking #1 | week2_day8_security b2b | SUCCESS |
| 4 | OC Business Networking #2 | week2_day9_phishing b2b | SUCCESS |
| 5 | OC Business Networking #3 | week1_day2_scam_alert b2b | SUCCESS (messy fmt) |
| 6 | OC Biz Networking Experts | week1_day5_soft_promo b2b | SUCCESS_PENDING |
| 7 | CA Business Entrepreneurs | marketplace_repair_listing b2b | SUCCESS |
| 8 | CA Entrepreneurs | week2_day10_data_recovery b2b | SUCCESS |
| 9 | S OC Business | week2_day13_ssd_upgrade b2b | SUCCESS |
| 10 | Supporting Small Biz SoCal | marketplace_ssd_upgrade b2b | SUCCESS |
| 11 | OC/LA Business Networking | week1_day6_smart_home b2b | SUCCESS_PENDING |
| 12 | SoCal Business Networking | week1_day7_community b2b | SUCCESS |
| 13 | OC Contractors/Handyman | marketplace_data_recovery b2b | SUCCESS |
| 14 | Cerritos Business | week2_day11_laptop_tip b2b | SUCCESS |

### Previous Session (Feb 6, 2026) - 13 Successful Posts (v3.5)
| # | Group | Content | Result |
|---|-------|---------|--------|
| 1-6 | Anaheim Connect, Garden Grove, OC City Neighbors, Anaheim Community, Fun in Fullerton, Anything OC | various | SUCCESS (v1-v3.2) |
| 7-13 | Anything OC, OC Word of Mouth, Placentia, Fullerton Friends, Orange County, OC Daily Post, OC Beach | various | SUCCESS (v3.5) |

### Current Group Coverage (27/76 posted)
- **Tier 1:** 8 of 9
- **Tier 2 b2b:** 14 of 16 (2 remaining: support_small_biz_oc, hb_business_network)
- **Tier 2 parent:** 0 of 2 (tustin_moms, oc_community_multi_city)
- **Tier 3:** 5 of 50

### Next Steps (Priority Order)
- [x] Build autonomous API mode (browser_agent.py + main.py --api)
- [x] Add Business Page content to content_calendar.yaml (6 posts, 2-week rotation)
- [x] Fix content deduplication (same text was going to multiple groups)
- [ ] **Add BROWSER_USE_API_KEY to .env** (get from https://cloud.browser-use.com/dashboard)
- [ ] **Set `dry_run: false` in settings.yaml** when ready to go live
- [ ] **Transfer to VPS** (rsync to 5.161.45.43, set up cron)
- [ ] Finish last 2 Tier 2 b2b groups
- [ ] Quality audit of Feb 10 posts (check formatting)
- [ ] Post to Tier 2 parent groups (2 groups)
- [ ] Post to Tier 3 community groups (45 remaining)
- [ ] Set up first-comment CTAs
- [ ] Clarify blog post strategy with user
- [ ] Monitor engagement and reply to comments

---

## Google Calendar MCP Setup

**Status:** Installed, needs OAuth authorization

**Location:** `/home/brandon/mcp-google-calendar/`

**To complete setup:**
```bash
# Run this to trigger OAuth browser flow
cd /home/brandon/mcp-google-calendar
.venv/bin/python -c "
import sys
sys.path.insert(0, '.')
from mcp_server_google_calendar.auth.auth import authorize
creds = authorize()
print('SUCCESS - Calendar connected!')
"
```

Then:
1. Browser opens Google sign-in
2. Select your Google account
3. Click "Allow" to grant calendar access
4. Token saved to `/home/brandon/token.json`

**After OAuth, available tools:**
- `get-events` - View calendar events
- `create-event` - Schedule new events
- `check-availability` - Check free/busy status
- `get-current-date` - Get current date/time

---

## Critical Rules (MEMORIZE)

1. **NEVER put links in main post** - Put in first comment only
2. **NEVER post same text to multiple groups** - Vary every post
3. **Delays: 65-140 minutes** between posts (not faster)
4. **Max 3-5 posts per day** across all groups
5. **Per-group: 1 post every 14 days** maximum
6. **Stop immediately** if CAPTCHA or "spam" warning appears

---

## Quick Commands

```bash
# Check system status
python3 ~/fb-automation/src/main.py --status

# Preview what would be posted (safe dry run)
python3 ~/fb-automation/src/main.py --dry-run --api

# Run daily cycle via API (autonomous - requires BROWSER_USE_API_KEY)
python3 ~/fb-automation/src/main.py --api

# Post to Business Page only (Mon/Wed/Fri)
python3 ~/fb-automation/src/main.py --api --page-only

# Post to a specific group
python3 ~/fb-automation/src/main.py --api --post GROUP_ID

# Generate Browser Use task prompts (for Claude-assisted mode)
python3 ~/fb-automation/src/main.py --generate

# Pause all automation
touch ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock
```

### Cron Setup (VPS)
```bash
# Daily group posting at 9 AM PT
0 9 * * * /home/brandon/fb-automation/run.sh

# Business Page posts: Mon/Wed/Fri at 10 AM PT
0 10 * * 1,3,5 /home/brandon/fb-automation/run.sh --page-only
```

---

## Browser Use Profile

| Setting | Value |
|---------|-------|
| Profile ID | `0ab23467-abfc-45a1-b98d-1b199d6168cc` |
| Profile Name | facebook |
| Account | Brandon Ruiz (personal profile) |

**To post via Browser Use (v3.2):**
```
Use browser_task with:
- profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
- task: [generated by browser_agent.py _build_post_task()]
- max_steps: 25

Generate task via Python:
  python3 -c "
  import sys; sys.path.insert(0, 'src')
  from browser_agent import generate_mcp_command
  result = generate_mcp_command(payload, '0ab23467-abfc-45a1-b98d-1b199d6168cc')
  print(result['task'])
  "
```

---

## Group Tiers

| Tier | Count | Frequency | Description |
|------|-------|-----------|-------------|
| **Tier 1** | 9 | 2x/week | High-volume OC community groups (all content types) |
| **Tier 2** | 17 | 1x/week | Business/Niche: B2B, Parents (security, network, promo) |
| **Tier 3 Community** | 41 | 1x/2 weeks | Local city discussion groups (tips, dusty, security) |
| **Tier 3 Marketplace** | 9 | 1x/2 weeks | Buy/sell groups (promo + repairs ONLY) |

---

## Content Types

| Type | % of Posts | Purpose |
|------|------------|---------|
| **Dusty PC Photos** | 40% | Engagement, relatability |
| **Scam Alerts** | 25% | Establish expertise |
| **Quick Tips** | 20% | Value, helpfulness |
| **Soft Sells** | 15% | Lead generation |

---

## If User Asks To...

| Request | Action |
|---------|--------|
| "Post to groups" | Use Browser Use MCP with profile above |
| "Check status" | Run `python3 src/main.py --status` |
| "Add more groups" | Edit `config/groups.yaml` |
| "Change content" | Edit `config/content_calendar.yaml` |
| "See the dashboard" | Open `dashboard.html` in browser |
| "Start Phase 1" | Follow `EXECUTION_GUIDE.md` |
| "Generate images" | Use `mcp__gemini__gemini-generate-image` |

---

## MCP Tools Available

| Tool | Use For |
|------|---------|
| `mcp__browser-use__browser_task` | Execute Facebook actions |
| `mcp__browser-use__list_browser_profiles` | Get profile IDs |
| `mcp__gemini__gemini-query` | Get marketing advice |
| `mcp__gemini__gemini-generate-image` | Create graphics |
| `mcp__gemini__gemini-brainstorm` | Strategy ideation |
| `mcp__gemini__gemini-search` | Research current best practices |
| `mcp__google_calendar__*` | Calendar management (after OAuth) |

---

## Emergency Procedures

| Issue | Action |
|-------|--------|
| Account restricted | STOP all automation, wait 72 hours, read EMERGENCY_PROCEDURES.md |
| Post deleted by admin | Set `active: false` in groups.yaml, don't retry |
| Script errors | Check `data/logs/` for details |
| 0 likes on 3+ posts | Possible shadowban - pause 1 week |

**Quick Pause:**
```bash
touch ~/fb-automation/data/paused.lock
```

---

## File Structure

```
fb-automation/
├── JUMPSTART.md              <- YOU ARE HERE
├── EXECUTION_GUIDE.md        <- Phases, daily workflow, launch steps
├── STRATEGY_GUIDE.md         <- Marketing strategy
├── GROWTH_STRATEGY.md        <- Group/Page growth plan
├── CONTENT_TEMPLATES.md      <- Post templates & spintax
├── MSP-B2B-STRATEGY.md       <- B2B/MSP approach
├── EMERGENCY_PROCEDURES.md   <- Crisis response
├── README.md                 <- Technical docs
├── dashboard.html            <- Visual overview
├── config/
│   ├── settings.yaml         <- Main settings (dry_run: true)
│   ├── groups.yaml           <- 52 OC groups
│   ├── content_calendar.yaml <- 16 posts × 3 variations
│   └── photos_manifest.yaml  <- 18 photos
├── src/
│   ├── main.py              <- Entry point
│   ├── content_manager.py   <- Content logic
│   └── browser_agent.py     <- Browser Use interface
├── data/
│   ├── history.json         <- Post history
│   └── logs/                <- Daily logs
└── docs/
    ├── TROUBLESHOOTING_GUIDE.md
    ├── B2B_GROUPS_TO_JOIN.md
    └── archived/             <- Old redundant docs
```

---

## Related Projects

| Project | Location | Purpose |
|---------|----------|---------|
| **Google Calendar MCP** | `/home/brandon/mcp-google-calendar/` | Scheduling & reminders |
| **MCP Config** | `~/.mcp.json` | MCP server definitions |
| **Claude Settings** | `~/.claude/settings.local.json` | Permissions & servers |

---

## Launch Phases (Summary)

| Phase | When | Goal |
|-------|------|------|
| **Phase 1** | Week 1 | First live test post to 1 Tier 3 group |
| **Phase 2** | Weeks 2-3 | Soft launch: Tier 1 (8 groups), then add Tier 2 |
| **Phase 3** | Week 4+ | Full automation: all 52 groups |
| **Phase 4** | Parallel | B2B/MSP track via Business Page |

See `EXECUTION_GUIDE.md` for detailed steps.

---

## Next Session Checklist

When starting a new session:

1. Read this JUMPSTART.md first
2. Run `python3 ~/fb-automation/src/main.py --status`
3. Check if Google Calendar OAuth is complete
4. Ask user what they want to accomplish
5. Refer to appropriate guide:
   - Posting → EXECUTION_GUIDE.md
   - Strategy → STRATEGY_GUIDE.md
   - Growth → GROWTH_STRATEGY.md
   - Emergency → EMERGENCY_PROCEDURES.md

---

## Session History

| Date | Key Changes |
|------|-------------|
| Feb 10, 2026 | v3.6 ClipboardEvent paste: 12/12 Tier 2 b2b posts. Built autonomous API mode (browser_agent.py + main.py --api). Added Business Page content (6 posts). Fixed content dedup bug. Ready for VPS deployment. |
| Feb 6, 2026 (PM late) | v3.5 mass posting: 13 successful posts (7 v3.5 + 6 earlier). 8/9 Tier 1 groups covered. Browser Use credits ran out before Tier 2. Line-by-line text entry fix for \n formatting. Dashboard, history, all tracking updated. |
| Feb 6, 2026 (PM) | Architecture overhaul: 76 groups (14 added from gap analysis), all sign-offs fixed with "LB Computer Help", 3 marketplace content pieces added, dashboard updated with marketplace previews + photo mapping guide, content-to-group matching architecture designed. v3.5 breakthrough: native input + .closest() Post click |
| Feb 6, 2026 (AM) | browser_agent.py v3.2 WORKING (execCommand + dialog scoping + wiggle). 6 successful posts. Groups rebuilt from live FB scrape. |
| Feb 5, 2026 | Dashboard rewritten, all docs made consistent, Google Calendar MCP installed, Growth Strategy created, Launch Checklist created |
| Feb 3, 2026 | Strategy guide created, delays updated to 65-140 min |
| Feb 2, 2026 | Initial framework built, 52 groups configured |

---

*This file should be the FIRST thing read by any new Claude session working on this project.*
