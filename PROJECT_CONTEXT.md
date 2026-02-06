# LB Computer Help - Facebook Automation Context

**Last Updated:** February 3, 2026
**Purpose:** Single source of truth to prevent confusion across multiple Claude sessions

---

## Quick Start for New Sessions

**READ FIRST:** `JUMPSTART.md` - Contains everything needed to continue this project

---

## Core Identity

| Item | Value |
|------|-------|
| **Business** | LB Computer Help - Computer Repair & MSP |
| **Location** | Orange County, CA (moved from Long Beach) |
| **Service Area** | OC ONLY (no longer LB/LA County) |
| **Brand Voice** | Helpful neighbor, not corporate |

### Marketing Strategy

| Track | Account | Purpose | Tone |
|-------|---------|---------|------|
| **Residential** | Personal (Brandon Ruiz) | One-off repairs | Helpful neighbor |
| **B2B/MSP** | Business Page | Monthly contracts | Professional |

**Key Insight:** Personal profile > Business page for community groups

---

## System Architecture

| Component | Details |
|-----------|---------|
| **Engine** | Python + Browser Use Cloud |
| **Browser Profile ID** | `0ab23467-abfc-45a1-b98d-1b199d6168cc` |
| **Config Location** | `/home/brandon/fb-automation/config/` |
| **Groups Source** | `groups.yaml` (52 OC groups) |
| **Posting Mode** | `dry_run: true` (safe until enabled) |

---

## Documentation Index

| File | Purpose | Priority |
|------|---------|----------|
| `JUMPSTART.md` | Quick start for new sessions | READ FIRST |
| `PROJECT_CONTEXT.md` | Business context (this file) | Reference |
| `STRATEGY_GUIDE.md` | Marketing strategy from research | Study |
| `EXECUTION_PLAN.md` | Daily/weekly workflow | Execute |
| `CONTENT_TEMPLATES.md` | Post templates with variations | Use |
| `EMERGENCY_PROCEDURES.md` | Crisis response guide | Keep handy |
| `README.md` | Technical documentation | Developers |

---

## Key Files Structure

```
fb-automation/
├── Documentation
│   ├── JUMPSTART.md          <- Start here for new sessions
│   ├── PROJECT_CONTEXT.md    <- Business context (this file)
│   ├── STRATEGY_GUIDE.md     <- Marketing research
│   ├── EXECUTION_PLAN.md     <- Daily workflow
│   ├── CONTENT_TEMPLATES.md  <- Post templates
│   ├── EMERGENCY_PROCEDURES.md <- Crisis response
│   └── README.md             <- Technical docs
│
├── Configuration
│   ├── config/settings.yaml      <- Main settings
│   ├── config/groups.yaml        <- 52 OC groups
│   ├── config/content_calendar.yaml <- Content pieces
│   └── config/photos_manifest.yaml  <- Photo inventory
│
├── Code
│   ├── src/main.py           <- Entry point
│   ├── src/content_manager.py <- Content logic
│   └── src/browser_agent.py  <- Browser Use interface
│
├── Data
│   ├── data/history.json     <- Post tracking
│   └── data/logs/            <- Execution logs
│
├── Assets
│   └── assets/logo_badge.jpg <- Generated logo
│
└── Tools
    └── dashboard.html        <- Visual dashboard
```

---

## Critical Rules (ALWAYS FOLLOW)

### Posting Rules
1. **Max 3-5 posts per day** across all groups
2. **Delay 65-140 minutes** between posts (randomized)
3. **Per-group: 1 post every 14 days** maximum
4. **NEVER put links in main post** - first comment only
5. **NEVER post identical content** to multiple groups

### Safety Rules
6. **STOP if CAPTCHA** appears - pause 24 hours
7. **STOP if "spam" warning** - pause 72 hours
8. **Engage 10:1** - 10 likes/comments per promotional post
9. **Leave groups slowly** - max 12/day when cleaning up

### Content Rules
10. **Sound like a neighbor** - not a business
11. **Use raw photos** - no graphics/text overlays
12. **Mention local cities** - builds trust
13. **Share helpful tips** - not just promotions

---

## Current Status (February 3, 2026)

| Metric | Value |
|--------|-------|
| Groups configured | 52 (OC-focused) |
| Content pieces | 16 posts x 3 variations |
| Posting mode | DRY RUN (safe) |
| Delays | 65-140 min (research-based) |

### Completed
- [x] Audit of all 231 Facebook groups
- [x] Configuration updated for OC only
- [x] Strategy research via Gemini
- [x] Documentation package created
- [x] Settings optimized per research
- [x] Cleanup of LB/LA groups (manually left all non-OC groups)

### In Progress
- [ ] Content expansion to 5+ variations

### Not Started
- [ ] First live test post
- [ ] Cron automation setup
- [ ] Enhanced Browser Use script

---

## Quick Commands

```bash
# Check status
python3 ~/fb-automation/src/main.py --status

# Preview posts (safe)
python3 ~/fb-automation/src/main.py --dry-run

# Generate Browser Use tasks
python3 ~/fb-automation/src/main.py --generate

# Enable live posting
# Edit config/settings.yaml: dry_run: false

# Pause automation
touch ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock
```

---

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `browser_task` | Execute FB actions |
| `monitor_task` | Watch task progress |
| `gemini-query` | Get advice |
| `gemini-search` | Research topics |
| `gemini-generate-image` | Create graphics |
| `gemini-brainstorm` | Collaborate on strategy |

---

## What NOT to Do

- Don't post same content to multiple groups
- Don't put links in main post text
- Don't post faster than 65 min intervals
- Don't ignore CAPTCHA or warnings
- Don't leave more than 12 groups per day
- Don't automate DMs or comments
- Don't run multiple Claude sessions simultaneously

---

## Emergency Quick Reference

| Situation | Action |
|-----------|--------|
| CAPTCHA shown | Pause 24 hours |
| "Spam" warning | Pause 72 hours |
| Account restricted | Stop everything, wait 72h, see EMERGENCY_PROCEDURES.md |
| Post deleted | Remove group from config |

---

## Change Log

| Date | Change |
|------|--------|
| Feb 5, 2026 | Manually left all non-OC groups - cleanup complete |
| Feb 3, 2026 | Complete documentation package created |
| Feb 3, 2026 | Settings updated: delays 65-140 min |
| Feb 3, 2026 | Groups reduced from 58 to 52 (OC only) |
| Feb 2, 2026 | Initial project setup |

---

*This file is the single source of truth. Update it when project status changes.*
