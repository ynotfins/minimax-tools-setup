# Database Ping - Read-Only Check
# Tests connectivity without making any writes

$Host = [Environment]::GetEnvironmentVariable("PGVECTOR_HOST") ?? "localhost"
$Port = [Environment]::GetEnvironmentVariable("PGVECTOR_PORT") ?? "5432"
$DB = [Environment]::GetEnvironmentVariable("PGVECTOR_DB") ?? "vector_db"
$User = [Environment]::GetEnvironmentVariable("PGVECTOR_USER") ?? "postgres"

Write-Host "=== Database Connection Test (Read-Only) ===" -ForegroundColor Cyan
Write-Host "Host: $Host"
Write-Host "Port: $Port"
Write-Host "Database: $DB"
Write-Host "User: $User"
Write-Host ""

try {
    # Test connection string
    $connString = "host=$Host port=$Port dbname=$DB user=$User"
    
    # Query vector count (read-only)
    $query = "SELECT COUNT(*) as vector_count FROM pgvector_read;"
    
    # Use psql for simple connection test
    $result = & "C:\Program Files\PostgreSQL\16\bin\psql.exe" `
        -h $Host `
        -p $Port `
        -U $User `
        -d $DB `
        -c $query `
        -t 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Connection successful" -ForegroundColor Green
        Write-Host "Vector count: $($result.Trim())"
    } else {
        Write-Host "[ERROR] Connection failed" -ForegroundColor Red
        Write-Host $result
    }
} catch {
    Write-Host "[ERROR] Exception: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Mode: READ_ONLY (no writes performed)"
