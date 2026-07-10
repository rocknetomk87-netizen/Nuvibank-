#!/data/data/com.termux/files/usr/bin/bash

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

pg_dump nuvibank > ~/NUVIBANK/backups/nuvibank_$TIMESTAMP.sql

echo "BACKUP CREATED:"
echo "$TIMESTAMP"
