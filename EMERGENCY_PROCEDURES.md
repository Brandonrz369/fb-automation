# LB Computer Help - Emergency Procedures

## Crisis Response Guide for Facebook Automation

**Last Updated:** February 3, 2026
**Purpose:** Immediate action steps when things go wrong

---

## Severity Levels

| Level | Indicator | Action |
|-------|-----------|--------|
| **CRITICAL** | Account restricted/banned | Stop everything immediately |
| **HIGH** | Multiple posts deleted, warnings | Pause 72 hours |
| **MEDIUM** | Single post deleted, CAPTCHA | Pause 24 hours |
| **LOW** | Low engagement, minor issues | Monitor and adjust |

---

## CRITICAL: Account Restricted

### Symptoms
- "Your account is restricted from posting"
- "We limit how often you can post"
- Can't access Facebook at all
- Logged out and can't log back in

### Immediate Actions (Within 5 Minutes)

```
1. STOP all automation immediately
   - Kill any running Browser Use tasks
   - Run: touch ~/fb-automation/data/paused.lock

2. DO NOT try to log in repeatedly
   - This makes it worse

3. Document the error
   - Screenshot the message
   - Note the exact time
   - Save to data/logs/incident_[DATE].md
```

### Recovery Process (24-72 Hours)

```
Hour 0-24:
- Do NOTHING with the account
- No logins, no attempts, nothing

Hour 24-48:
- Log in ONCE from your phone (not automation)
- Just scroll feed, like a friend's post
- Log out

Hour 48-72:
- Log in again normally
- Light activity only (like, comment on friends)
- No business activity

After 72 hours:
- Check if restrictions are lifted
- If yes, resume at 50% volume (2 posts/day max)
- If no, wait another 72 hours
```

### If Permanently Banned
1. Do NOT create new accounts (they'll be linked)
2. Appeal through Facebook's official process
3. Consider pivoting to Business Page only
4. Document lessons learned

---

## HIGH: Multiple Posts Deleted / Admin Warnings

### Symptoms
- 2+ posts deleted in one day
- Message from group admin
- "Your post goes against our community standards"
- Multiple groups remove you

### Immediate Actions

```
1. Pause automation for 72 hours
   Run: touch ~/fb-automation/data/paused.lock

2. Review which posts were deleted
   - Check data/history.json
   - Note the groups and content

3. Identify the pattern
   - Same content posted too fast?
   - Link in main post?
   - Promotional language?

4. Update groups.yaml
   - Set active: false for problem groups
   - Add to "banned" notes
```

### Recovery Process

```
Day 1-3:
- Manual activity only
- Engage as normal user (no business posts)
- Like and comment on others' content

Day 4-7:
- Resume with ONE post per day
- Only to groups that didn't delete posts
- Completely different content

Day 8+:
- Gradually increase to normal volume
- Monitor closely for any issues
```

---

## MEDIUM: Single Post Deleted / CAPTCHA

### Symptoms
- One post deleted by admin
- Facebook shows CAPTCHA
- "Are you a robot?" verification
- Temporary slowdown message

### Immediate Actions

```
1. Complete the CAPTCHA (if shown)
   - Solve it carefully
   - Don't fail multiple times

2. Pause automation for 24 hours
   Run: touch ~/fb-automation/data/paused.lock

3. Review the deleted post
   - What group?
   - What content?
   - Against their rules?

4. Remove problem group
   Edit config/groups.yaml - set active: false
```

### Recovery Process

```
After 24 hours:
- Resume normal activity
- Skip the problem group permanently
- Monitor next few posts closely
```

---

## LOW: Low Engagement / Minor Issues

### Symptoms
- Posts getting 0 likes consistently
- Fewer comments than usual
- Possible shadowban

### Diagnostic Steps

```
1. Check if posts are visible
   - Log out
   - View group as public
   - Can you see your recent posts?

2. If posts NOT visible (Shadowban):
   - Pause posting for 1 week
   - Increase engagement on others' posts
   - Vary content significantly

3. If posts ARE visible (Just low engagement):
   - Review content quality
   - Check posting times
   - Try different content types
```

### Recovery Process

```
Week 1:
- Post 50% less frequently
- Engage 2x more on others' content
- Use completely fresh content

Week 2:
- Monitor engagement
- If improving, slowly increase
- If not, continue reduced activity
```

---

## Technical Failures

### Browser Use Script Errors

```
Symptom: Script crashes, doesn't complete
Action:
1. Check data/logs/ for error details
2. Verify Browser Use profile still valid
3. Test with manual browser task first
4. Report issue if persists
```

### Login Session Expired

```
Symptom: "Please log in" during automation
Action:
1. Stop automation
2. Manually log in from phone
3. Check for security alerts
4. Re-authenticate Browser Use profile
5. Resume cautiously
```

### Wrong Group Posted To

```
Symptom: Content posted to wrong group
Action:
1. Delete the post immediately (if possible)
2. Check groups.yaml for URL errors
3. Verify content_manager.py logic
4. Test with --dry-run before resuming
```

---

## Communication Templates

### If Admin Messages You

```
Response template:

"Hi! Sorry about that - I'm a local computer repair tech
just trying to help neighbors with tech tips. If my post
wasn't appropriate for this group, I totally understand.
Won't happen again. Thanks for letting me know!"
```

### If User Complains About Spam

```
Response template:

"Hey, really sorry if my post felt spammy - definitely
not my intention. Just trying to share helpful info.
I'll tone it down. Appreciate the feedback!"
```

---

## Prevention Checklist

### Daily
- [ ] Check for any Facebook notifications/warnings
- [ ] Verify posts appeared correctly
- [ ] Monitor engagement levels

### Weekly
- [ ] Review groups.yaml for any problem groups
- [ ] Check history.json for patterns
- [ ] Update content if getting stale

### Monthly
- [ ] Full audit of automation health
- [ ] Review and update strategy
- [ ] Check Facebook's latest policy changes

---

## Emergency Contacts

| Issue | Resource |
|-------|----------|
| Facebook Account Help | facebook.com/help |
| Appeal Form | facebook.com/help/contact/260749603972907 |
| Browser Use Support | Check MCP documentation |
| Claude Code Issues | github.com/anthropics/claude-code |

---

## Quick Commands

```bash
# PAUSE all automation immediately
touch ~/fb-automation/data/paused.lock

# Check if paused
ls ~/fb-automation/data/paused.lock

# Resume automation
rm ~/fb-automation/data/paused.lock

# Check recent logs
tail -100 ~/fb-automation/data/logs/latest.log

# See posting history
cat ~/fb-automation/data/history.json | python3 -m json.tool
```

---

## Incident Log Template

Save to `data/logs/incident_YYYY-MM-DD.md`:

```markdown
# Incident Report - [DATE]

## Summary
[Brief description of what happened]

## Timeline
- [TIME]: First noticed issue
- [TIME]: Actions taken
- [TIME]: Resolution/current status

## Root Cause
[What caused the issue]

## Impact
- Posts affected: [NUMBER]
- Groups affected: [LIST]
- Account status: [STATUS]

## Resolution
[What fixed it or current status]

## Prevention
[What to do differently]
```

---

*Keep this document handy. When emergencies happen, you won't have time to figure things out.*
