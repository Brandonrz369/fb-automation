# LB Computer Help - Implementation Runbook

**Version:** 1.0
**Created:** February 2, 2026
**Purpose:** Week-by-week execution plan for Facebook automation launch

---

## Overview

### Two-Track System

| Track | Account | Automation Level | Timeline |
|-------|---------|------------------|----------|
| **Residential** | Personal (Brandon) | High - automated posting | Weeks 1-4 |
| **B2B/MSP** | Business Page | Low - manual/guided | Weeks 3-6 |

### Project Status Summary (Updated Feb 5, 2026)

| Component | Readiness | Notes |
|-----------|-----------|-------|
| Framework Code | 100% | Ready for testing |
| Groups Config | 100% | 52 OC groups configured |
| Content Library | 100% | 16 posts × 3 variations = 48 |
| Photo Assets | 100% | 18 photos cataloged |
| Group Cleanup | 100% | Left all non-OC groups |
| Scheduling | 0% | Needs cron setup |
| B2B Track | 20% | Strategy documented |

---

## Phase 1: Proof of Concept (Week 1)

### Goal
Verify the automation framework works end-to-end with a single test post.

### Day 1-2: Environment Validation

- [ ] **Verify Python environment**
  ```bash
  cd ~/fb-automation
  python3 --version  # Should be 3.8+
  pip3 install -r requirements.txt
  ```

- [ ] **Test framework loads**
  ```bash
  python3 src/main.py --status
  ```
  Expected: Shows group counts, content stats, no errors

- [ ] **Verify Browser Use profile**
  - Profile ID: `0ab23467-abfc-45a1-b98d-1b199d6168cc`
  - Test with simple task in Claude Code

### Day 3-4: Dry Run Testing

- [ ] **Preview content selection**
  ```bash
  python3 src/main.py --dry-run
  ```
  Expected: Shows which groups would receive which content

- [ ] **Verify content matching**
  - Check that community groups get community variations
  - Check that B2B groups get b2b variations
  - Verify photo suggestions are appropriate

- [ ] **Review generated Browser Use tasks**
  ```bash
  python3 src/main.py --generate
  ```
  Expected: Outputs ready-to-use Browser Use prompts

### Day 5-7: First Live Post

- [ ] **Select test group** (low-risk, active)
  - Recommended: A Tier 3 group you're already active in
  - NOT a large Tier 1 group

- [ ] **Execute manual post via Browser Use**
  ```
  Use browser_task with:
  - profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
  - task: [paste generated task]
  - max_steps: 15
  ```

- [ ] **Verify post appeared**
  - Check the group manually
  - Screenshot for documentation

- [ ] **Document any issues**
  - Note timing, errors, unexpected behavior
  - Add to TROUBLESHOOTING_GUIDE.md

### Success Criteria
- [ ] Framework runs without errors
- [ ] Content selection logic works correctly
- [ ] At least 1 post successfully published
- [ ] Photo uploaded with post (if applicable)

### Go/No-Go Decision
If all criteria met → Proceed to Phase 2
If issues found → Document and fix before proceeding

---

## Phase 2: Soft Launch - Residential Track (Weeks 2-3)

### Goal
Begin regular posting to Tier 1 groups, monitor engagement, refine approach.

### Week 2: Tier 1 Groups (8 groups)

#### Daily Tasks

| Day | Groups | Content Focus |
|-----|--------|---------------|
| Mon | 2 Tier 1 | Tips/Educational |
| Tue | 2 Tier 1 | Behind-the-scenes |
| Wed | 2 Tier 1 | Security/Scam alert |
| Thu | 2 Tier 1 | Tips/Educational |
| Fri | Review | Check engagement, respond to comments |

#### Execution Method
```bash
# Generate today's posts
python3 src/main.py --generate

# Execute each via Browser Use (manual approval)
# Use Claude Code to run browser_task for each
```

#### Monitoring Checklist
- [ ] Check each group within 2 hours of posting
- [ ] Respond to ALL comments
- [ ] Note which content gets most engagement
- [ ] Screenshot any leads/inquiries

### Week 3: Expand + Optimize

#### Add Tier 2 Groups (12 groups)

| Day | Tier 1 | Tier 2 | Total Posts |
|-----|--------|--------|-------------|
| Mon | 2 | 1 | 3 |
| Tue | 2 | 1 | 3 |
| Wed | 2 | 1 | 3 |
| Thu | 2 | 1 | 3 |
| Fri | Review & Respond | - | - |

#### Content Refinement
- [ ] Identify top 3 performing post types
- [ ] Create 5 new variations of winners
- [ ] Retire underperforming content
- [ ] Update content_calendar.yaml

### Success Criteria
- [ ] 20+ posts published without account issues
- [ ] Average 5+ engagements per post
- [ ] At least 2 lead inquiries
- [ ] No group removals or warnings

---

## Phase 3: Full Automation - Residential Track (Weeks 4-6)

### Goal
Enable automated scheduling, expand to all 52 groups, set up monitoring.

### Week 4: Enable Automation

#### Switch to Automated Mode
```yaml
# config/settings.yaml
safety:
  dry_run: false  # Enable live posting
```

#### Set Up Cron (Local or VPS)
```bash
# Edit crontab
crontab -e

# Add daily run at 9 AM
0 9 * * * /home/brandon/fb-automation/run.sh
```

#### Daily Monitoring Routine
- [ ] Check logs: `~/fb-automation/data/logs/`
- [ ] Review posts in groups (spot check 3-5)
- [ ] Respond to comments within 2 hours
- [ ] Note any issues in log

### Week 5: Scale to Tier 3

#### Add All Configured Groups
- Tier 1: 8 groups (daily)
- Tier 2: 12 groups (3x/week)
- Tier 3: 32 groups (rotating 1/day)

#### Posting Volume Target
| Week | Posts/Day | Groups Active |
|------|-----------|---------------|
| 4 | 3-4 | 20 |
| 5 | 4-5 | 40 |
| 6 | 5 | 52 |

### Week 6: Optimize & Maintain

#### Performance Review
- [ ] Which groups drive most engagement?
- [ ] Which content types perform best?
- [ ] Any groups to remove (low engagement, strict rules)?
- [ ] Need more content variations?

#### Create Performance Dashboard
Track weekly:
- Posts published
- Total engagements
- Comments responded to
- Leads generated
- Conversion rate

### Success Criteria
- [ ] Automation running 5+ days without manual intervention
- [ ] 50+ posts per week across all tiers
- [ ] Consistent engagement (5+ per post average)
- [ ] 5+ leads per week
- [ ] Zero account warnings

---

## Phase 4: B2B/MSP Track Launch (Weeks 3-6)

### Goal
Establish Business Page presence in professional groups for MSP client acquisition.

### Week 3-4: Foundation

#### Identify Target Groups
- [ ] Research 10-15 OC business networking groups
- [ ] Verify Business Page can join (some require personal)
- [ ] Prioritize by member count and activity

**Recommended Groups to Find:**
- OC Small Business Owners
- Orange County Entrepreneurs
- SoCal Business Networking
- OC Chamber of Commerce groups
- Industry-specific (dental, legal, real estate)

#### Join Groups (Business Page)
- [ ] Join 5 groups first week
- [ ] Join 5 more second week
- [ ] Wait 48 hours before posting

### Week 5: Soft Launch B2B

#### Create B2B Content (5 posts minimum)
1. Problem/Solution post (network failure story)
2. Security alert (current threat)
3. Case study (anonymized client win)
4. Thought leadership (3 IT mistakes)
5. Introduction post (for new groups)

#### Posting Schedule
| Day | Action |
|-----|--------|
| Mon | Post to 1 business group |
| Wed | Post to 1 business group |
| Fri | Review, respond, engage |

### Week 6: Relationship Building

#### Engagement Focus
- [ ] Comment on other posts (helpful, not salesy)
- [ ] Answer IT questions when asked
- [ ] Connect with business owners via DM (if appropriate)
- [ ] Track all conversations

#### Lead Tracking
Create spreadsheet with:
- Business name
- Contact name
- Group source
- Inquiry date
- Follow-up status
- Outcome

### Success Criteria
- [ ] 10+ business groups joined
- [ ] 10+ B2B posts published
- [ ] 5+ meaningful conversations
- [ ] 1+ consultation booked

---

## Ongoing Operations (Week 7+)

### Daily Routine (15 min)
1. Check automation logs
2. Spot check 3-5 posts
3. Respond to comments/messages
4. Note any issues

### Weekly Review (30 min)
1. Review engagement metrics
2. Identify top content
3. Plan next week's special content
4. Check for new group opportunities

### Monthly Tasks
1. Create new content (10+ posts)
2. Catalog new photos
3. Review group performance
4. Adjust tier assignments
5. Expand to new groups

---

## Risk Mitigation

### Account Safety
- Never exceed 5 posts/hour
- Randomize posting times (±30 min)
- Respond to comments personally
- Follow all group rules
- Take breaks on weekends if needed

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Post failed | Check logs, retry manually |
| Account restricted | Pause automation, post manually for 1 week |
| Group removed post | Review rules, adjust content |
| Low engagement | Test different content types |
| Browser Use timeout | Increase max_steps, simplify task |

### Emergency Pause
```bash
# Create pause file to stop automation
touch ~/fb-automation/data/paused.lock

# Check why automation paused
cat ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock
```

---

## File Checklist

### Phase 1 Deliverables
- [x] PROJECT_CONTEXT.md
- [x] IMPLEMENTATION_RUNBOOK.md (this file)
- [ ] TROUBLESHOOTING_GUIDE.md

### Phase 2 Deliverables
- [ ] METRICS_AND_TRACKING.md
- [ ] Extended content (10+ new posts)

### Phase 3 Deliverables
- [ ] VPS_DEPLOYMENT_GUIDE.md
- [ ] GROUP_EXPANSION_PLAN.md

### Phase 4 Deliverables
- [x] MSP-B2B-STRATEGY.md
- [ ] B2B_CONTENT_LIBRARY.md
- [ ] LEAD_TRACKING_SPREADSHEET

---

## Quick Reference

### Key Commands
```bash
# Status check
python3 src/main.py --status

# Preview posts (dry run)
python3 src/main.py --dry-run

# Generate Browser Use tasks
python3 src/main.py --generate

# Run automation (after enabling)
./run.sh
```

### Key Files
```
~/fb-automation/
├── config/settings.yaml      # Enable/disable automation
├── config/groups.yaml        # Group whitelist
├── config/content_calendar.yaml  # Post content
├── data/history.json         # What was posted
└── data/logs/                # Daily logs
```

### Browser Use Profile
```
Profile ID: 0ab23467-abfc-45a1-b98d-1b199d6168cc
Account: Brandon Ruiz (Personal)
```

---

*Last Updated: February 2, 2026*
