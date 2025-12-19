#!/bin/sh

PYTHON=/usr/local/bin/python
SCRIPT=/app/revenue_prediction.py
LOG=/var/log/ml.log

cat <<EOF | crontab -
* * * * * cd /app && $PYTHON $SCRIPT >> $LOG 2>&1
EOF

# Ensure log file exists and is writable
touch /var/log/ml.log
chmod 666 /var/log/ml.log

# Start cron in foreground
cron -f
