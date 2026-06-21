# Disaster Recovery

## Recovery Scenarios

### Scenario 1: pgvector Service Down

1. Check service status:
   ```powershell
   Get-Service postgresql*
   ```

2. If stopped, attempt restart:
   ```powershell
   Start-Service postgresql-x64-16
   ```

3. Check logs in PostgreSQL data directory

4. If service won't start:
   - Check disk space on E: drive
   - Check PostgreSQL logs
   - Attempt manual recovery from backup

### Scenario 2: Corrupted Vector Data

1. Stop PostgreSQL service
2. Restore from last known good backup
3. Verify integrity:
   ```sql
   SELECT COUNT(*) FROM pgvector_read;
   ```

### Scenario 3: External Drive Failure

1. If E: drive fails:
   - Reinstall PostgreSQL on new drive
   - Restore from backup

2. If F: drive fails:
   - Reinstall pgvector extension
   - Re-enable extension in postgresql.conf

### Scenario 4: Complete System Loss

1. **Prerequisite**: Off-site backup available
2. Reinstall Windows
3. Install PostgreSQL 16
4. Restore configuration
5. Restore database from backup
6. Verify all services

## Recovery Time Objectives

| Scenario | RTO | RPO |
|----------|-----|-----|
| Service down | 30 min | 24 hours |
| Corrupted data | 2 hours | 24 hours |
| Drive failure | 4 hours | 24 hours |
| Complete loss | 8 hours | 24 hours |

## Emergency Contacts

- Database issues: Check PostgreSQL community forums
- pgvector issues: Check pgvector GitHub issues
- Windows issues: Windows support

## Pre-disaster Checklist

- [ ] Backups verified and tested
- [ ] Configuration files backed up
- [ ] Emergency procedures documented
- [ ] Recovery media available
- [ ] Off-site backup location secured
