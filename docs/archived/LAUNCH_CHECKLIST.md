# LB Computer Help - Launch Checklist

**Created:** February 5, 2026
**Purpose:** Step-by-step checklist to go from dry-run to live posting

---

## Pre-Launch Status

| Component | Status | Notes |
|-----------|--------|-------|
| Framework Code | ✅ Complete | Python scripts tested |
| Groups Config | ✅ Complete | 52 OC groups configured |
| Content Library | ✅ Complete | 16 posts × 3 variations |
| Photo Assets | ✅ Complete | 18 photos cataloged |
| Group Cleanup | ✅ Complete | Left all non-OC groups |
| Safety Settings | ✅ Complete | dry_run: true, 65-140 min delays |
| Documentation | ✅ Complete | All docs updated and consistent |
| Growth Strategy | ✅ Complete | Group/Page growth plan ready |

---

## Phase 1: First Live Test (This Week)

### Day 1: Final Verification
- [ ] Run `python3 ~/fb-automation/src/main.py --status` - verify counts
- [ ] Run `python3 ~/fb-automation/src/main.py --dry-run` - preview posts
- [ ] Verify Browser Use profile still works (test simple navigation)
- [ ] Choose a LOW-RISK Tier 3 group for first test

**Suggested test group:** One where you're already active and have posted manually before.

### Day 2: First Live Post
- [ ] Generate task: `python3 ~/fb-automation/src/main.py --generate`
- [ ] Execute ONE post via Browser Use MCP:
  ```
  Use browser_task with:
  - profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
  - task: [paste generated task]
  - max_steps: 15
  ```
- [ ] Verify post appeared in group
- [ ] Screenshot for documentation
- [ ] Record in history.json (or confirm automation did)

### Day 3: Monitor & Evaluate
- [ ] Check for engagement (likes, comments)
- [ ] Respond to any comments
- [ ] Check for admin warnings or post removal
- [ ] Note any issues in log

**GO/NO-GO Decision:**
- Post appeared correctly? → Proceed to Phase 2
- Issues found? → Document and fix before continuing

---

## Phase 2: Soft Launch (Week 2-3)

### Week 2: Tier 1 Groups Only (8 groups)

**Daily Schedule:**
| Day | Action | Groups |
|-----|--------|--------|
| Mon | Post to 2 Tier 1 groups | Santa Ana Neighbors, Anything OC |
| Tue | Post to 2 Tier 1 groups | Cypress Community, Fullerton Friends |
| Wed | Post to 2 Tier 1 groups | HB Community Forum, Westminster |
| Thu | Post to 2 Tier 1 groups | Anaheim Connect, Placentia Regional |
| Fri | Review engagement, respond to comments | - |
| Sat | Rest / catch up | - |
| Sun | Plan next week's content | - |

**Daily Tasks:**
- [ ] Generate posts: `python3 src/main.py --generate`
- [ ] Execute via Browser Use (manual approval each post)
- [ ] Wait 65-140 minutes between posts
- [ ] Check posts within 2 hours, respond to comments
- [ ] Log any issues

### Week 3: Add Tier 2 Groups (+12 groups)

**Posting volume:** 3-4 posts/day
- 2 Tier 1 groups
- 1-2 Tier 2 groups (B2B, Parent groups)

**Weekly Checklist:**
- [ ] 15-20 posts published
- [ ] Average 3+ engagements per post
- [ ] At least 1 DM inquiry
- [ ] Zero account warnings
- [ ] Zero posts removed by admins

---

## Phase 3: Full Automation (Week 4+)

### Enable Live Mode

1. **Edit settings.yaml:**
   ```bash
   nano ~/fb-automation/config/settings.yaml
   ```
   Change:
   ```yaml
   safety:
     dry_run: false  # Change from true to false
   ```

2. **Test automated cycle:**
   ```bash
   python3 ~/fb-automation/src/main.py
   ```

3. **Set up cron (optional):**
   ```bash
   crontab -e
   # Add:
   0 9 * * * /home/brandon/fb-automation/run.sh
   ```

### Daily Monitoring Routine (15 min/day)
- [ ] Check logs: `tail -50 ~/fb-automation/data/logs/automation_$(date +%Y-%m-%d).log`
- [ ] Spot check 3-5 posts in groups
- [ ] Respond to comments/DMs
- [ ] Note any issues

### Weekly Review (30 min)
- [ ] Total posts this week
- [ ] Engagement metrics
- [ ] Leads generated
- [ ] Any groups to remove/add
- [ ] Content performing best

---

## Phase 4: Business Page & Group (Parallel)

### Facebook Group Setup
- [ ] Create/rename group: "OC Tech Help & Computer Tips"
- [ ] Set privacy: Private but Visible
- [ ] Add membership questions:
  - "Do you live in Orange County?"
  - "What's your biggest computer frustration?"
- [ ] Write About description (see GROWTH_STRATEGY.md)
- [ ] Invite existing contacts

### Business Page Schedule
| Day | Content Type | Status |
|-----|--------------|--------|
| Monday | "Horror Photo" (dusty PC) | [ ] Scheduled |
| Wednesday | Scam Alert or Quick Tip | [ ] Scheduled |
| Friday | Behind the Scenes | [ ] Scheduled |

### Cross-Promotion
- [ ] Add soft CTAs to first comments on community posts
- [ ] Start "Tech Tuesday" Q&A loop
- [ ] Spend 15 min/day commenting helpfully in community groups

---

## Emergency Procedures

### If Account Warning Appears
1. STOP immediately: `touch ~/fb-automation/data/paused.lock`
2. Do NOT try to log in repeatedly
3. Wait 24-72 hours
4. See EMERGENCY_PROCEDURES.md

### If Post Removed by Admin
1. Note which group and content
2. Set `active: false` for that group in groups.yaml
3. Continue with other groups
4. Don't retry that group

### Quick Pause Command
```bash
# Pause everything
touch ~/fb-automation/data/paused.lock

# Resume
rm ~/fb-automation/data/paused.lock
```

---

## Success Metrics

### Week 1 (Test)
- [ ] 1+ successful live post
- [ ] No account issues

### Week 2-3 (Soft Launch)
- [ ] 20+ posts published
- [ ] 5+ average engagements
- [ ] 2+ DM inquiries
- [ ] 0 warnings

### Month 1 (Full Automation)
- [ ] 80+ posts published
- [ ] 5+ leads generated
- [ ] 1+ job booked from Facebook
- [ ] 0 account restrictions

### Month 2+ (Growth)
- [ ] Facebook Group: 50+ members
- [ ] Business Page: 100+ followers
- [ ] 10+ leads/month
- [ ] Consistent revenue from FB

---

## Quick Reference Commands

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

# Check logs
tail -50 ~/fb-automation/data/logs/automation_$(date +%Y-%m-%d).log

# Open dashboard
firefox ~/fb-automation/dashboard.html
```

---

## File Quick Reference

| Need To... | Edit This File |
|------------|----------------|
| Enable live posting | `config/settings.yaml` → `dry_run: false` |
| Add/remove groups | `config/groups.yaml` |
| Add new content | `config/content_calendar.yaml` |
| Add new photos | `config/photos_manifest.yaml` |
| See posting history | `data/history.json` |
| Check for pause | `data/paused.lock` |

---

*This checklist should be your guide from dry-run to full automation. Check off items as you complete them.*
