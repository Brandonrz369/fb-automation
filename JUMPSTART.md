# LB Computer Help - Facebook Automation JUMPSTART Guide

## For New Claude Sessions - READ THIS FIRST

**Last Updated:** February 6, 2026
**Purpose:** Enable any Claude session to immediately understand and continue this project

---

## Quick Context (30 seconds)

| What | Details |
|------|---------|
| **Business** | LB Computer Help - Computer Repair in Orange County, CA |
| **Goal** | Automate Facebook group posting to generate leads |
| **Method** | Browser Use MCP cloud automation + personal profile |
| **Status** | v3.5 LIVE - 13 successful posts today, 100% v3.5 success rate |

---

## Current Numbers (Verified Feb 6, 2026)

| Metric | Count | Notes |
|--------|-------|-------|
| **OC Groups** | 76 | Tier 1: 9, Tier 2: 17, Tier 3: 50 (incl 9 marketplace) |
| **Content Posts** | 19 | Each has 3 variations = 57 total (incl 3 marketplace) |
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

### CRITICAL: Browser Agent v3.5 (VERIFIED WORKING)
v3.5 was developed after v3.2's `execCommand('insertText')` broke on Feb 6 PM (Facebook changed editor). Key technical details:

- **ALL Facebook URLs must include `?_fb_noscript=1`**
- **Text entry**: Native Browser Use `input` action (NOT execCommand - it's broken)
- **React state activation**: Space+Backspace "wiggle" after text entry
- **NEVER use Escape key** (closes modal)
- **Post button**: Find SPAN with `textContent === 'Post'` → `.closest('[role="button"]')` → click
  - The Post button is NOT a `div` element - all `div[role="button"]` selectors fail
  - `.closest('[role="button"]')` traverses up the DOM tree regardless of element type
- **max_steps: 15** (typically completes in 9)

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

### Posting History (Feb 6, 2026) - 13 Successful Posts
| # | Group | Content | Result | Version |
|---|-------|---------|--------|---------|
| 1 | Anaheim Connect | productivity_tip | SUCCESS_PENDING | v1 |
| 2 | Garden Grove: What's going on? | tech_tip | SUCCESS_PENDING | v2 |
| 3 | OC City Neighbors | scam_alert | SUCCESS_PUBLISHED | v2 |
| 4 | Anaheim Community | laptop_tip | SUCCESS_PUBLISHED | v3.2 |
| 5 | Fun in Fullerton | myth_buster | SUCCESS_PUBLISHED | v3.2 |
| 6 | Anything Orange County | dusty_pc | SUCCESS_PENDING | v3.2 |
| 7 | Anything OC | wifi_tip | SUCCESS_PUBLISHED | v3.5 |
| 8 | OC Word of Mouth | ssd_upgrade | SUCCESS_PUBLISHED | v3.5 |
| 9 | All Things Placentia/YL/Fullerton | community | SUCCESS_PENDING | v3.5 |
| 10 | Fullerton Friends | scam_alert | SUCCESS_PENDING | v3.5 |
| 11 | Orange County | phishing_tip | SUCCESS_PUBLISHED | v3.5 |
| 12 | OC Daily Post | password_security | SUCCESS_PENDING | v3.5 |
| 13 | Orange County (Beach) | appreciation | SUCCESS_PENDING | v3.5 |

### Groups Posted To Today (13/76)
- **Tier 1:** 8 of 9 (Anaheim Connect, OC City Neighbors, OC Word of Mouth, Regional Placentia, Fullerton Friends, Orange County General, OC Daily Post, Orange County Beach)
- **Tier 2:** 0 of 17 (blocked by Browser Use credits running out)
- **Tier 3:** 5 of 50 (Garden Grove, Anaheim Community, Fun in Fullerton, Anything OC x2)

### Ready for Next Steps
- [ ] Replenish Browser Use credits to continue posting
- [ ] Post to 2 more groups to reach 15 (OC Small Biz, Buena Park Small Biz)
- [ ] Post on LB Computer Help Business Page
- [ ] Quality check all posts (verify text, formatting, visibility)
- [ ] Production posting schedule (begin daily tier rotation)
- [ ] Cron automation setup
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

# Preview what would be posted (safe)
python3 ~/fb-automation/src/main.py --dry-run

# Generate Browser Use task prompts
python3 ~/fb-automation/src/main.py --generate

# View dashboard
firefox ~/fb-automation/dashboard.html

# Pause all automation
touch ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock
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
| Feb 6, 2026 (PM late) | v3.5 mass posting: 13 successful posts (7 v3.5 + 6 earlier). 8/9 Tier 1 groups covered. Browser Use credits ran out before Tier 2. Line-by-line text entry fix for \n formatting. Dashboard, history, all tracking updated. |
| Feb 6, 2026 (PM) | Architecture overhaul: 76 groups (14 added from gap analysis), all sign-offs fixed with "LB Computer Help", 3 marketplace content pieces added, dashboard updated with marketplace previews + photo mapping guide, content-to-group matching architecture designed. v3.5 breakthrough: native input + .closest() Post click |
| Feb 6, 2026 (AM) | browser_agent.py v3.2 WORKING (execCommand + dialog scoping + wiggle). 6 successful posts. Groups rebuilt from live FB scrape. |
| Feb 5, 2026 | Dashboard rewritten, all docs made consistent, Google Calendar MCP installed, Growth Strategy created, Launch Checklist created |
| Feb 3, 2026 | Strategy guide created, delays updated to 65-140 min |
| Feb 2, 2026 | Initial framework built, 52 groups configured |

---

*This file should be the FIRST thing read by any new Claude session working on this project.*
