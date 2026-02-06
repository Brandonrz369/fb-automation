# LB Computer Help - Facebook Automation JUMPSTART Guide

## For New Claude Sessions - READ THIS FIRST

**Last Updated:** February 5, 2026
**Purpose:** Enable any Claude session to immediately understand and continue this project

---

## Quick Context (30 seconds)

| What | Details |
|------|---------|
| **Business** | LB Computer Help - Computer Repair in Orange County, CA |
| **Goal** | Automate Facebook group posting to generate leads |
| **Method** | Browser Use MCP cloud automation + personal profile |
| **Status** | All config complete, ready for first live post |

---

## Current Numbers (Verified Feb 5, 2026)

| Metric | Count | Notes |
|--------|-------|-------|
| **OC Groups** | 52 | Tier 1: 8, Tier 2: 12, Tier 3: 32 |
| **Content Posts** | 16 | Each has 3 variations = 48 total |
| **Photos** | 18 | Categorized by type |
| **Delay Between Posts** | 65-140 min | Random, mimics human behavior |
| **Max Posts/Day** | 3-5 | Safety limit |
| **Per-Group Frequency** | 1x per 14 days | Avoid spam detection |

---

## Key Files to Read (Priority Order)

```
1. JUMPSTART.md           <- YOU ARE HERE
2. EXECUTION_GUIDE.md     <- Phases, daily workflow, launch steps
3. STRATEGY_GUIDE.md      <- Research-backed posting strategy
4. GROWTH_STRATEGY.md     <- Growing Group/Page + Business Page content
5. config/settings.yaml   <- Current automation settings
6. config/groups.yaml     <- 52 OC groups to post to
```

---

## Current State (February 5, 2026)

### What's Complete
- [x] 52 Orange County groups configured in groups.yaml
- [x] 16 content pieces with 3 variations each (48 total)
- [x] Settings updated with safe delays (65-140 min)
- [x] Strategy guide created from Gemini research
- [x] 18 photos categorized and ready
- [x] Cleanup of all non-OC groups complete
- [x] Dashboard.html fully updated with accurate data
- [x] All documentation consolidated (Feb 5)
- [x] Growth strategy for Group/Page created
- [x] Browser agent upgraded: pre-engagement scroll+like, first-comment CTAs
- [x] Redundant docs consolidated into EXECUTION_GUIDE.md
- [x] Google Calendar MCP installed (optional - for reminders)

### Ready for Next Steps
- [ ] First live test post (Phase 1 in EXECUTION_GUIDE.md)
- [ ] Content variations expansion (5+ per post)
- [ ] Cron automation setup
- [ ] Google Calendar OAuth (optional, for Tech Tuesday reminders)

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

**To post via Browser Use:**
```
Use browser_task with:
- profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
- task: [paste generated task from --generate]
- max_steps: 15
```

---

## Group Tiers

| Tier | Count | Description | Examples |
|------|-------|-------------|----------|
| **Tier 1** | 8 | High-volume community groups | Santa Ana Neighbors, Anything OC |
| **Tier 2** | 12 | Niche: B2B, Parents, Local | OC Parents, Business Networks |
| **Tier 3** | 32 | Local city groups | Irvine, Fullerton, HB, etc. |

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
| Feb 5, 2026 | Dashboard rewritten, all docs made consistent, Google Calendar MCP installed, Growth Strategy created, Launch Checklist created |
| Feb 3, 2026 | Strategy guide created, delays updated to 65-140 min |
| Feb 2, 2026 | Initial framework built, 52 groups configured |

---

*This file should be the FIRST thing read by any new Claude session working on this project.*
