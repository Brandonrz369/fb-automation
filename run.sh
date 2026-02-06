#!/bin/bash
# ============================================
# LB Computer Help - Facebook Automation Runner
# ============================================
#
# This script is designed to be called by cron for automated execution.
#
# Cron example (runs daily at 9 AM):
#   0 9 * * * /home/brandon/fb-automation/run.sh
#
# For VPS deployment, you may need to:
#   1. Set up a Python virtual environment
#   2. Configure any necessary display for headed browser
#   3. Set environment variables for API keys
#

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Create log directory if it doesn't exist
mkdir -p data/logs

# Set timestamp for this run
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="data/logs/run_${TIMESTAMP}.log"

echo "============================================" >> "$LOG_FILE"
echo "FB Automation Run: $TIMESTAMP" >> "$LOG_FILE"
echo "============================================" >> "$LOG_FILE"

# Run the main script
python3 src/main.py >> "$LOG_FILE" 2>&1

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Run completed successfully" >> "$LOG_FILE"
else
    echo "Run failed with exit code: $EXIT_CODE" >> "$LOG_FILE"
fi

echo "============================================" >> "$LOG_FILE"

# Optional: Send notification on failure
# if [ $EXIT_CODE -ne 0 ]; then
#     # Send email, Slack message, etc.
#     echo "Automation failed!" | mail -s "FB Automation Error" your@email.com
# fi

exit $EXIT_CODE
