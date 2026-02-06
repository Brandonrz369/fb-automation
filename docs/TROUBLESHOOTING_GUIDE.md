# LB Computer Help - Troubleshooting Guide

**Purpose:** Quick solutions for common issues with Facebook automation

---

## Quick Diagnostics

### Check System Status
```bash
cd ~/fb-automation
python3 src/main.py --status
```

### Check for Pause File
```bash
ls -la ~/fb-automation/data/paused.lock
# If exists, automation is paused
cat ~/fb-automation/data/paused.lock  # See reason
```

### Check Recent Logs
```bash
ls -lt ~/fb-automation/data/logs/ | head -5
cat ~/fb-automation/data/logs/run_YYYY-MM-DD_*.log
```

---

## Common Issues & Solutions

### 1. Framework Won't Start

**Symptom:** `python3 src/main.py` fails with import error

**Solutions:**
```bash
# Install dependencies
pip3 install -r requirements.txt

# Verify Python version (need 3.8+)
python3 --version

# Check you're in right directory
cd ~/fb-automation
pwd
```

---

### 2. "No Eligible Content for Group"

**Symptom:** Dry run shows no content for a group

**Causes:**
- All matching content already posted to that group
- Content tags don't match group's content_tags
- Content calendar is empty

**Solutions:**
```bash
# Check posting history
cat data/history.json | python3 -m json.tool | head -50

# Reset history for a group (careful!)
# Edit data/history.json and remove entries for that group

# Verify content tags match
grep -A5 "group_name" config/groups.yaml
grep "category:" config/content_calendar.yaml
```

---

### 3. Browser Use Task Fails

**Symptom:** Browser Use times out or can't find elements

**Solutions:**

1. **Increase max_steps**
   ```
   max_steps: 20  # Instead of 10
   ```

2. **Use Vision Mode**
   - Facebook has obfuscated class names
   - Browser Use's vision mode identifies elements visually
   - Should be enabled by default

3. **Simplify the task**
   - Break into smaller steps
   - Test navigation separately from posting

4. **Check Profile Session**
   - Profile ID: `0ab23467-abfc-45a1-b98d-1b199d6168cc`
   - Session may have expired
   - Re-authenticate if needed

---

### 4. Automation Paused Unexpectedly

**Symptom:** `paused.lock` file exists

**Causes:**
- 3+ consecutive failures
- Manual pause
- Error during execution

**Solutions:**
```bash
# Check why it paused
cat ~/fb-automation/data/paused.lock

# If issue resolved, remove pause file
rm ~/fb-automation/data/paused.lock

# Check last log for errors
cat ~/fb-automation/data/logs/run_$(date +%Y-%m-%d)*.log
```

---

### 5. Post Didn't Appear in Group

**Symptom:** Browser Use reported success but post isn't visible

**Causes:**
- Group moderation queue
- Post was flagged/removed
- Browser Use clicked wrong button

**Solutions:**
1. Check group's "Your Posts" or "Pending Posts"
2. Review group rules - may have violated them
3. Check if post is in history.json
4. Run manually and watch live session

---

### 6. Wrong Content Variation Used

**Symptom:** B2B group got community-style post

**Causes:**
- Group's `audience_segment` set incorrectly
- Content doesn't have that variation

**Solutions:**
```yaml
# Check group config
# config/groups.yaml
- id: "some_group"
  audience_segment: "b2b"  # Should match content variation

# Check content has variation
# config/content_calendar.yaml
variations:
  community: "..."
  b2b: "..."      # Must exist
  parent: "..."
```

---

### 7. Photo Not Uploading

**Symptom:** Post publishes but without image

**Causes:**
- Photo path incorrect
- File doesn't exist
- Browser Use can't find upload button

**Solutions:**
```bash
# Verify photo exists
ls -la ~/fb-automation/assets/photos/IMG_1810.jpg

# Check photos_manifest.yaml has correct path
grep "base_path" config/settings.yaml

# Test photo upload separately
# Use Browser Use to just upload a photo, not post
```

---

### 8. Rate Limiting / Account Warning

**Symptom:** Facebook shows warning or limits actions

**Immediate Actions:**
1. **STOP all automation immediately**
   ```bash
   touch ~/fb-automation/data/paused.lock
   echo "Facebook rate limit warning" > ~/fb-automation/data/paused.lock
   ```

2. **Wait 24-48 hours** before any posting

3. **Post manually** for 1 week to look human

4. **Reduce frequency** when resuming
   ```yaml
   # config/settings.yaml
   posting:
     max_posts_per_day: 2  # Reduce from 5
   ```

---

### 9. Cron Job Not Running

**Symptom:** Automation doesn't run at scheduled time

**Solutions:**
```bash
# Check cron is installed and running
systemctl status cron

# View current crontab
crontab -l

# Check cron log
grep CRON /var/log/syslog | tail -20

# Verify run.sh is executable
chmod +x ~/fb-automation/run.sh

# Test run.sh manually
~/fb-automation/run.sh
```

---

### 10. History File Corrupted

**Symptom:** JSON parse errors, weird behavior

**Solutions:**
```bash
# Validate JSON
python3 -c "import json; json.load(open('data/history.json'))"

# If corrupted, backup and reset
cp data/history.json data/history.json.backup
echo '{}' > data/history.json
```

---

## Facebook-Specific Issues

### Anti-Bot Detection

**Symptoms:**
- CAPTCHAs appearing
- "Unusual activity" warnings
- Login challenges

**Prevention:**
- Use random delays between posts (already configured)
- Don't post more than 5/hour
- Vary posting times slightly
- Keep human engagement (comments, reactions)

### Group Rules Violations

**Symptoms:**
- Post removed by admins
- Warning from group
- Removed from group

**Prevention:**
- Read each group's rules before adding
- Avoid promotional content in strict groups
- Wait 48+ hours after joining before first post
- Contribute value before promoting

---

## Debug Mode

### Enable Verbose Logging
```python
# In src/main.py, add at top:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Content Selection
```bash
python3 -c "
from pathlib import Path
from src.content_manager import ContentManager
cm = ContentManager(Path('config'), Path('data'))
print(cm.get_stats())
for g in cm.select_groups_for_today():
    print(f'{g[\"name\"]}: {cm.generate_post_payload(g)}')
"
```

### Watch Browser Use Live
When running Browser Use tasks, the live_url shows real-time browser:
```
https://live.browser-use.com?wss=...
```
Open this URL to watch what the browser is doing.

---

## Getting Help

### Information to Gather
Before asking for help, collect:
1. Error message (exact text)
2. Last 50 lines of log file
3. Contents of paused.lock (if exists)
4. Result of `--status` command
5. What you were trying to do

### Log File Location
```bash
~/fb-automation/data/logs/run_YYYY-MM-DD_HH-MM-SS.log
```

---

## Recovery Procedures

### Full Reset (Nuclear Option)
```bash
# Backup current state
cp -r ~/fb-automation/data ~/fb-automation/data.backup.$(date +%Y%m%d)

# Reset history
echo '{}' > ~/fb-automation/data/history.json

# Remove pause
rm -f ~/fb-automation/data/paused.lock

# Clear logs
rm -f ~/fb-automation/data/logs/*.log
```

### Restore from Backup
```bash
# If something went wrong
cp -r ~/fb-automation/data.backup.YYYYMMDD/* ~/fb-automation/data/
```

---

*Last Updated: February 2, 2026*
