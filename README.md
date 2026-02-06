# LB Computer Help - Facebook Automation Framework

Automated Facebook group posting system using Browser Use cloud automation.

## Quick Start

### 1. Check Status
```bash
cd ~/fb-automation
python3 src/main.py --status
```

### 2. Preview Today's Posts (Dry Run)
```bash
python3 src/main.py --dry-run
```

### 3. Generate Posts for Manual Execution
```bash
python3 src/main.py --generate
```

This outputs Browser Use task prompts you can execute via Claude Code.

### 4. Enable Live Posting
Edit `config/settings.yaml`:
```yaml
safety:
  dry_run: false  # Change from true to false
```

## Directory Structure

```
fb-automation/
├── config/
│   ├── settings.yaml          # Main settings (Browser Use profile, posting limits)
│   ├── groups.yaml            # Facebook groups configuration
│   ├── content_calendar.yaml  # Post content with audience variations
│   └── photos_manifest.yaml   # Photo inventory with categories
├── data/
│   ├── history.json           # Tracks what was posted where
│   └── logs/                  # Execution logs
├── src/
│   ├── main.py               # Entry point
│   ├── content_manager.py    # Content selection logic
│   └── browser_agent.py      # Browser Use interface
├── run.sh                    # Cron execution script
└── requirements.txt
```

## How It Works

### Content Matching
1. Each **group** has `content_tags` (e.g., `["dusty", "repairs", "tips"]`)
2. Each **post** has a `category` (e.g., `"dusty"`)
3. The system matches posts to groups based on tags
4. Each post has 3 **variations**: `community`, `b2b`, `parent`
5. The group's `audience_segment` determines which variation to use

### Photo Selection
1. Posts can have `suggested_photos` for specific images
2. Otherwise, photos are matched by `category`
3. Photos with lower `used_count` are preferred (rotation)

### History Tracking
- `data/history.json` tracks every post
- Content is never repeated to the same group
- When all content is exhausted for a group, it's skipped

## Configuration

### Adding New Groups
Edit `config/groups.yaml`:
```yaml
- id: "new_group_id"
  name: "Group Display Name"
  url: "https://www.facebook.com/groups/groupname"
  audience_segment: "community"  # or "b2b" or "parent"
  content_tags: ["dusty", "repairs", "tips"]
  tier: 2  # 1=daily, 2=every other day, 3=weekly rotation
  active: true
```

### Adding New Content
Edit `config/content_calendar.yaml`:
```yaml
- id: "unique_post_id"
  day: 15
  category: "dusty"
  suggested_photos: ["IMG_1810.jpg"]
  variations:
    community: "Community version of the post..."
    b2b: "Business version of the post..."
    parent: "Parent-focused version..."
```

### Adding New Photos
1. Copy photo to the photos directory
2. Add entry to `config/photos_manifest.yaml`:
```yaml
- filename: "new_photo.jpg"
  category: "repairs"
  description: "Description of the photo"
  quality: "excellent"
  used_count: 0
```

## VPS Deployment

### 1. Install Dependencies
```bash
cd ~/fb-automation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Up Cron
```bash
crontab -e
# Add line:
0 9 * * * /home/brandon/fb-automation/run.sh
```

### 3. Browser Use Cloud API (Optional)
For fully autonomous VPS operation, you'll need to:
1. Get a Browser Use Cloud API key
2. Set environment variable: `export BROWSER_USE_API_KEY=your_key`
3. Update `browser_agent.py` to use API mode

## Safety Features

- **Dry Run Mode**: Default is `dry_run: true` - nothing posts until you enable it
- **Pause File**: Create `data/paused.lock` to stop all automation
- **Max Failures**: After 3 consecutive failures, automation pauses automatically
- **Random Delays**: 65-140 minute random delays between posts (research-based humanization)

## Manual Execution via Claude Code

To post manually, run:
```bash
python3 src/main.py --generate
```

Then in Claude Code, use the Browser Use MCP:
```
Use browser_task with:
- profile_id: 0ab23467-abfc-45a1-b98d-1b199d6168cc
- task: [paste the generated task]
- max_steps: 15
```

## Troubleshooting

### "No eligible content for group"
- All content matching that group's tags has been posted
- Add new content or reset history

### Automation paused
- Check `data/paused.lock` for reason
- Delete the file to resume

### Logs
- Check `data/logs/` for detailed execution logs
