#!/bin/bash
# ============================================
# LB Computer Help - Facebook Automation Runner
# ============================================
#
# Cron examples (using flock to prevent overlap, timeout for safety):
#
#   # Daily group posting at 9 AM PT (kill if runs >2 hours)
#   0 9 * * * /usr/bin/flock -n /tmp/fb_cron.lock /usr/bin/timeout 7200 /root/fb-automation/run.sh
#
#   # Business Page posts: Mon/Wed/Fri at 10 AM PT
#   0 10 * * 1,3,5 /usr/bin/flock -n /tmp/fb_page.lock /usr/bin/timeout 3600 /root/fb-automation/run.sh --page-only
#

# Navigate to project directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

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
    # Ping healthcheck on success (set HEALTHCHECK_URL in .env)
    if [ -n "$HEALTHCHECK_URL" ]; then
        curl -fsS -m 10 --retry 3 "$HEALTHCHECK_URL" > /dev/null 2>&1
    fi
else
    echo "Run failed with exit code: $EXIT_CODE" >> "$LOG_FILE"
    # Ping healthcheck failure endpoint
    if [ -n "$HEALTHCHECK_URL" ]; then
        curl -fsS -m 10 --retry 3 "${HEALTHCHECK_URL}/fail" > /dev/null 2>&1
    fi
fi

echo "============================================" >> "$LOG_FILE"

exit $EXIT_CODE
