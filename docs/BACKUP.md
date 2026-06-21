# Backup Guide

## Overview

This guide covers backup procedures for the MiniMax agent stack including pgvector database and configuration files.

## Backup Schedule

| Component | Frequency | Retention |
|-----------|-----------|-----------|
| PostgreSQL DB | Daily | 7 days |
| Config files | Weekly | 4 weeks |
| Full system image | Monthly | 3 months |

## Backup Commands

### PostgreSQL Database Backup
```bash
# Create a plain SQL backup
pg_dump -h localhost -U postgres -d vector_db -F p -f backup.sql

# Compressed binary backup
pg_dump -h localhost -U postgres -d vector_db -F c -Z 5 -f backup.dump
```

### Restore from Backup
```bash
# Restore from plain SQL
psql -h localhost -U postgres -d vector_db -f backup.sql

# Restore from compressed
pg_restore -h localhost -U postgres -d vector_db -c backup.dump
```

## External Drive Backup

### Database Files (E: Drive)
```powershell
# Backup entire data directory
Robocopy E:\postgres_data E:\backups\postgres_$(Get-Date -Format "yyyyMMdd") /MIR /R:3
```

### Vector Extensions (F: Drive)
```powershell
# Backup extensions
Robocopy F:\pgvector_ext F:\backups\pgvector_$(Get-Date -Format "yyyyMMdd") /MIR /R:3
```

## Automated Backups

See `scripts/pg_dump_backup.ps1` for automated daily backups.

## Verification

Always verify backups by restoring to a test environment:
```bash
# Test restore
pg_restore --dbname=vector_db_test backup.dump
```
