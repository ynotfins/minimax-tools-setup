# PostgreSQL Backup Script
# Run daily via Task Scheduler

param(
    [string]$BackupDir = "E:\backups\postgres",
    [int]$RetentionDays = 7
)

$Date = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = Join-Path $BackupDir "vector_db_$Date.dump"

# Ensure backup directory exists
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force
}

Write-Host "Starting PostgreSQL backup..."
Write-Host "Backup file: $BackupFile"

# Run pg_dump
& "C:\Program Files\PostgreSQL\16\bin\pg_dump.exe" `
    -h localhost `
    -U postgres `
    -d vector_db `
    -F c `
    -Z 5 `
    -f $BackupFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup completed successfully: $BackupFile"
    
    # Cleanup old backups
    $CutoffDate = (Get-Date).AddDays(-$RetentionDays)
    Get-ChildItem $BackupDir -Filter "*.dump" | 
        Where-Object { $_.LastWriteTime -lt $CutoffDate } |
        Remove-Item -Force
    
    Write-Host "Old backups cleaned up."
} else {
    Write-Error "Backup failed with exit code: $LASTEXITCODE"
    exit 1
}
