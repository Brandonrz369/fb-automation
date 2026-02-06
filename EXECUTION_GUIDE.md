# LB Computer Help - Execution Guide

**Last Updated:** February 5, 2026
**Purpose:** Single reference for launching and running the automation (replaces LAUNCH_CHECKLIST, EXECUTION_PLAN, IMPLEMENTATION_RUNBOOK, and PHASE_OVERVIEW)

---

## Current Status

| Component | Status |
|-----------|--------|
| Framework Code | Ready |
| Groups Config | 52 OC groups (Tier 1: 8, Tier 2: 12, Tier 3: 32) |
| Content Library | 16 posts x 3 variations = 48 total |
| Photo Assets | 18 photos cataloged |
| Safety Settings | dry_run: true, 65-140 min delays |
| Posting Mode | DRY RUN (safe until manually enabled) |

---

## Phase 1: First Live Test (This Week)

### Pre-Flight Checks
```bash
python3 ~/fb-automation/src/main.py --status    # Verify counts
python3 ~/fb-automation/src/main.py --dry-run   # Preview posts
```

### Test Post Execution
1. Pick a LOW-RISK Tier 3 group you're already active in
2. Generate the task:
   ```bash
   python3 ~/fb-automation/src/main.py --generate
   ```
3. Execute ONE post via Browser Use MCP:
   ```
   profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
   max_steps: 25
   task: [paste generated task]
   ```
4. Verify post appeared in the group
5. Monitor for 24 hours - check engagement, admin warnings

**GO/NO-GO:** Post appeared correctly? Proceed to Phase 2. Issues? Fix first.

---

## Phase 2: Soft Launch (Weeks 2-3)

### Week 2: Tier 1 Groups Only (8 groups)

| Day | Action | Posts |
|-----|--------|-------|
| Mon-Thu | Post to 2 groups/day | 2 |
| Fri | Review engagement, respond to comments | 0 |
| Sat-Sun | Rest / plan next week | 0 |

### Week 3: Add Tier 2 Groups (+12 groups)

| Day | Tier 1 | Tier 2 | Total |
|-----|--------|--------|-------|
| Mon-Thu | 2 | 1-2 | 3-4 |
| Fri | Review | - | 0 |

### Daily Tasks
- Generate posts: `python3 src/main.py --generate`
- Execute via Browser Use (manual approval each post)
- Wait 65-140 min between posts
- Check posts within 2 hours, respond to comments

### Weekly Success Criteria
- [ ] 15-20 posts published
- [ ] 3+ average engagements per post
- [ ] At least 1 DM inquiry
- [ ] Zero account warnings
- [ ] Zero posts removed by admins

---

## Phase 3: Full Automation (Week 4+)

### Enable Live Mode
```yaml
# config/settings.yaml
safety:
  dry_run: false
```

### Set Up Cron (Optional)
```bash
crontab -e
# Add: 0 9 * * * /home/brandon/fb-automation/run.sh
```

### Daily Monitoring (15 min)
- [ ] Spot check 3-5 posts in groups
- [ ] Respond to comments/DMs
- [ ] Note any issues

### Weekly Review (30 min)
- [ ] Total posts, engagement metrics, leads
- [ ] Groups to remove/add
- [ ] Best performing content

---

## Phase 4: Business Page & Group (Parallel)

### Facebook Group Setup
- Create/rename: "OC Tech Help & Computer Tips"
- Privacy: Private but Visible
- Membership questions: "Do you live in OC?", "Biggest computer frustration?"

### Business Page Schedule (3x/week)

| Day | Content Type |
|-----|--------------|
| Monday | "Horror Photo" (dusty PC) |
| Wednesday | Scam Alert or Quick Tip |
| Friday | Behind the Scenes |

### Tech Tuesday Loop
1. **Tuesday AM** - Post Q&A in Business Group: "What tech issue is annoying you this week?"
2. **Tuesday PM** - Answer best question on Business Page
3. **Wednesday** - Share answer to community groups

### Cross-Promotion
- Add soft CTAs to first comments on community posts (automated)
- Spend 15 min/day commenting helpfully in community groups
- Search groups for keywords: "laptop slow", "computer broken", "virus", "tech help"

---

## Daily Schedule (When Fully Automated)

### Morning (8:00-9:30 AM PT)
| Time | Action |
|------|--------|
| 8:00 | Login via Browser Use, scroll feed |
| 8:10 | Like 5-10 random posts (human signal) |
| 8:30 | Reply to any comments from yesterday |

### Distribution (10:00 AM - 2:00 PM PT)
| Time | Action |
|------|--------|
| 10:00 | Post #1 |
| 11:30 | Post #2 (~90 min delay) |
| 1:00 | Post #3 (~90 min delay) |

### Engagement (4:00-6:00 PM PT)
| Time | Action |
|------|--------|
| 4:00 | Check all posts for comments |
| 4:30 | Reply to questions, move leads to DM |
| 5:00 | Like posts in target groups |

### Evening (7:00-9:00 PM PT - Optional)
| Time | Action |
|------|--------|
| 7:00 | Post #4 (if quota not met) |
| 8:30 | Post #5 (final window) |

---

## Weekly Content Rotation

| Day | Content Type | Example |
|-----|--------------|---------|
| Monday | Educational Tip | "Why your laptop is slow..." |
| Tuesday | Dusty Computer Photo | Before/after cleaning |
| Wednesday | Security Warning | "Watch out for this scam..." |
| Thursday | Success Story | "Saved a student's thesis..." |
| Friday | Soft Promotion | "3 slots open this weekend..." |
| Saturday | Engagement Post | "What's your biggest tech frustration?" |
| Sunday | Rest / Catch-up | Only if behind on quota |

---

## Group Rotation System

With 52 groups and 4 posts/day, each group gets posted to every ~13 days.

### Content Batching
| Batch | Groups | Post Day |
|-------|--------|----------|
| A | Groups 1-10 | Monday |
| B | Groups 11-21 | Tuesday |
| C | Groups 22-32 | Wednesday |
| D | Groups 33-42 | Thursday |
| E | Groups 43-52 | Friday |

### Rules
- Never post to same group twice in 14 days
- Check history.json before posting
- Skip group if posted recently

---

## Success Metrics

### Week 1 (Test)
- 1+ successful live post, no account issues

### Weeks 2-3 (Soft Launch)
- 20+ posts, 5+ avg engagements, 2+ DM inquiries, 0 warnings

### Month 1 (Full Automation)
- 80+ posts, 5+ leads, 1+ job booked from FB, 0 restrictions

### Month 2+ (Growth)
- Facebook Group: 50+ members
- Business Page: 100+ followers
- 10+ leads/month

---

## Quick Commands

```bash
# Check status
python3 ~/fb-automation/src/main.py --status

# Preview posts (safe)
python3 ~/fb-automation/src/main.py --dry-run

# Generate Browser Use tasks
python3 ~/fb-automation/src/main.py --generate

# Run automation (requires dry_run: false)
python3 ~/fb-automation/src/main.py

# Pause automation
touch ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock
```

---

## Emergency Quick Reference

| Issue | Action |
|-------|--------|
| CAPTCHA | Pause 24 hours |
| "Spam" warning | Pause 72 hours |
| Account restricted | Stop everything, see EMERGENCY_PROCEDURES.md |
| Post deleted by admin | Set `active: false` for group, don't retry |
| 0 likes on 3+ posts | Possible shadowban - pause 1 week |

```bash
# Emergency pause
touch ~/fb-automation/data/paused.lock
```

---

*This guide consolidates LAUNCH_CHECKLIST.md, EXECUTION_PLAN.md, IMPLEMENTATION_RUNBOOK.md, and PHASE_OVERVIEW.md into a single reference.*
