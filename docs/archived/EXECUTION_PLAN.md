# LB Computer Help - Execution Plan

## Detailed Daily & Weekly Workflow

**Last Updated:** February 3, 2026
**Source:** Gemini Brainstorm + Research Synthesis

---

## Daily Schedule (Automated)

### Morning Cycle (8:00 AM - 9:30 AM PT)

| Time | Action | Purpose |
|------|--------|---------|
| 8:00 | Login via Browser Use | Establish session |
| 8:05 | Scroll feed 2-3 minutes | Warm-up activity |
| 8:10 | Like 5-10 random posts | Human behavior signal |
| 8:15 | Check notifications | Monitor engagement |
| 8:30 | Reply to any comments | Lead capture |

### Distribution Cycle (10:00 AM - 2:00 PM PT)

| Time | Action | Details |
|------|--------|---------|
| 10:00 | Post #1 | First group of the day |
| 11:30 | Post #2 | 90 min delay |
| 1:00 | Post #3 | 90 min delay |

### Engagement Cycle (4:00 PM - 6:00 PM PT)

| Time | Action | Purpose |
|------|--------|---------|
| 4:00 | Check all posts for comments | Find leads |
| 4:30 | Reply to questions | Move to DM |
| 5:00 | Like posts in target groups | Build presence |

### Evening Cycle (7:00 PM - 9:00 PM PT)

| Time | Action | Details |
|------|--------|---------|
| 7:00 | Post #4 (optional) | If quota not met |
| 8:30 | Post #5 (optional) | Final post window |

---

## Weekly Content Schedule

| Day | Content Type | Example |
|-----|--------------|---------|
| **Monday** | Educational Tip | "Why your laptop is slow..." |
| **Tuesday** | Dusty Computer Photo | Before/after cleaning |
| **Wednesday** | Security Warning | "Watch out for this scam..." |
| **Thursday** | Success Story | "Saved a student's thesis..." |
| **Friday** | Soft Promotion | "3 slots open this weekend..." |
| **Saturday** | Engagement Post | "What's your biggest tech frustration?" |
| **Sunday** | Rest / Catch-up | Only if behind on quota |

---

## Group Rotation System

With 52 groups and 4 posts/day, each group gets posted to every ~13 days.

### Tier A Groups (Post First)
High-engagement community groups:
- Neighbors of Santa Ana (106K members)
- Anything Orange County (68K members)
- Huntington Beach Community Forum
- Westminster Community Forum

### Tier B Groups (Secondary)
Buy/sell and classifieds:
- Huntington Beach For Sale
- Cypress CA buy & sell
- Various marketplace groups

### Tier C Groups (Rotation)
Smaller city-specific groups:
- Individual city community groups
- Neighborhood-specific groups

---

## Content Batching System

### Batch Structure (5 Batches)

| Batch | Groups | Post Day |
|-------|--------|----------|
| A | Groups 1-10 | Monday |
| B | Groups 11-21 | Tuesday |
| C | Groups 22-32 | Wednesday |
| D | Groups 33-42 | Thursday |
| E | Groups 43-52 | Friday |

### Rotation Rules
- Never post to same group twice in 14 days
- Check history.json before posting
- Skip group if posted recently

---

## Pre-Post Checklist (Every Post)

```
[ ] Navigate to group
[ ] Scroll feed 30-60 seconds
[ ] Like 1 random post
[ ] Check last post date to this group
[ ] Verify content hasn't been used in 48 hours
[ ] Post content (no links in main text)
[ ] Add link in first comment (if needed)
[ ] Wait 65-140 minutes before next post
```

---

## KPIs to Track

### Daily Metrics
| Metric | Target | Red Flag |
|--------|--------|----------|
| Posts completed | 3-5 | <3 |
| Comments received | 2+ | 0 for 3 days |
| DMs received | 1+ | 0 for 5 days |
| Posts deleted | 0 | >1 |

### Weekly Metrics
| Metric | Target | Red Flag |
|--------|--------|----------|
| Total posts | 20-25 | <15 |
| New leads | 5+ | <2 |
| Groups banned from | 0 | >2 |
| Engagement rate | 2%+ | <0.5% |

### Monthly Metrics
| Metric | Target | Action |
|--------|--------|--------|
| Appointments booked | 10+ | Review content if low |
| Revenue from FB | Track | Compare to effort |
| Account warnings | 0 | Review strategy if any |

---

## Browser Use Task Template

```
Post to Facebook Group - [GROUP NAME]

1. Navigate to [GROUP URL]
2. Wait 3 seconds for page load
3. Scroll down slowly (2 page lengths)
4. Find and like 1 random post
5. Click "Write something..." or post button
6. Upload photo from [PHOTO PATH]
7. Paste this text (DO NOT include any links):

[POST TEXT HERE]

8. Click Post
9. Wait 5 seconds
10. Add comment with link: "More info: [LINK]"
11. Verify post appeared
12. Report success/failure
```

---

## Spintax Template System

To avoid duplicate detection, use these variations:

### Greetings
```
{Hey|Hi|Hello|What's up} {OC|Orange County|neighbors|everyone|folks}!
```

### Closings
```
{Stay safe|Take care|Cheers|Have a great day}! {🔧|💻|✨|}
```

### Call to Action
```
{DM me|Send me a message|Drop a comment|Reach out} {if interested|for details|to learn more}!
```

### Example Spun Post
```
{Hey|Hi|Hello} {OC|Orange County} {neighbors|folks}!

{Opened up|Just cleaned|Worked on} a {laptop|computer|PC} for a {neighbor|client|customer} in {[CITY]} today.

{This is what|Here's what|Check out what} {3|4|5} years of {dust|pet hair|neglect} does to your {cooling fan|internals|components}!

If your {laptop|computer} {sounds like a jet engine|runs hot|is super slow}, this {might be|is probably|could be} why.

{Easy fix|Quick cleanup|Simple solution} - {runs quiet now|good as new|back to normal}!

{DM me|Send a message|Comment below} if you need help with yours!
```

---

## Automation Health Checks

### Daily (Automated)
- [ ] All scheduled posts completed
- [ ] No error logs
- [ ] Account not restricted

### Weekly (Manual)
- [ ] Review engagement metrics
- [ ] Check for admin warnings
- [ ] Update content if stale
- [ ] Verify delays are randomized

### Monthly (Strategic)
- [ ] Review ROI of time spent
- [ ] Archive low-performing groups
- [ ] Add new groups if needed
- [ ] Update strategy based on results

---

## Quick Reference Commands

```bash
# Morning check
python3 src/main.py --status

# See what would post today
python3 src/main.py --dry-run

# Generate tasks for Browser Use
python3 src/main.py --generate

# Check logs
tail -50 data/logs/latest.log

# Pause automation
touch data/paused.lock

# Resume automation
rm data/paused.lock
```

---

*Follow this plan consistently for best results. Adjust based on engagement data.*
