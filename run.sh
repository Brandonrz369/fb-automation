#!/bin/bash
# ============================================
# LB Computer Help - Facebook Automation Runner
# ============================================
#
# Cron examples:
#   # Daily group posting at 9 AM PT
#   0 9 * * * /home/brandon/fb-automation/run.sh
#
#   # Business Page posts: Mon/Wed/Fri at 10 AM PT
#   0 10 * * 1,3,5 /home/brandon/fb-automation/run.sh --page-only
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
echo "Args: $@" >> "$LOG_FILE"
echo "============================================" >> "$LOG_FILE"

# Run the main script in API mode (autonomous)
python3 src/main.py --api "$@" >> "$LOG_FILE" 2>&1

# Capture exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Run completed successfully" >> "$LOG_FILE"
else
    echo "Run failed with exit code: $EXIT_CODE" >> "$LOG_FILE"
fi

echo "============================================" >> "$LOG_FILE"

exit $EXIT_CODE
