#!/bin/bash

docker exec pg_audio pg_dump -U yolistenHEAD yolistenDB > backups/backup_$(date +%Y%m%d_%H%M%S).sql

echo "Backup created: backups/backup_$(date +%Y%m%d_%H%M%S).sql"


# chmod +x scripts/backup.sh
# run ./scripts/backup.sh