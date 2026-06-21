# Environment Variable Audit Script
# Lists all environment variables without exposing secrets

Write-Host "=== MiniMax Agent Tools - Environment Audit ===" -ForegroundColor Cyan
Write-Host ""

# Check for required variables (without showing values)
$RequiredVars = @(
    "PGVECTOR_HOST",
    "PGVECTOR_PORT", 
    "PGVECTOR_DB",
    "PGVECTOR_USER",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY"
)

$OptionalVars = @(
    "PGVECTOR_PASSWORD",  # Should be set but not shown
    "LOG_LEVEL",
    "READ_ONLY_MODE"
)

Write-Host "Required Variables:" -ForegroundColor Yellow
foreach ($var in $RequiredVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        Write-Host "  [OK] $var" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $var" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Optional Variables:" -ForegroundColor Yellow
foreach ($var in $OptionalVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        if ($var -match "KEY|PASSWORD|SECRET") {
            Write-Host "  [SET] $var = ********" -ForegroundColor Green
        } else {
            Write-Host "  [SET] $var = $value" -ForegroundColor Green
        }
    } else {
        Write-Host "  [NOT SET] $var" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=== Audit Complete ==="
