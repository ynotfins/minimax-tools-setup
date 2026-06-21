# Frequent Commit Helper
# Run after completing each task to commit and push changes

param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

$RepoRoot = "D:\minimax-tools-setup"

Set-Location $RepoRoot

Write-Host "=== Frequent Commit ===" -ForegroundColor Cyan
Write-Host "Message: $Message"
Write-Host ""

# Stage all changes
git add -A

# Check if there are changes
$status = git status --porcelain
if ($status) {
    Write-Host "Changes detected, committing..." -ForegroundColor Yellow
    
    git commit -m $Message
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Committed successfully" -ForegroundColor Green
        
        # Push to remote
        Write-Host "Pushing to remote..." -ForegroundColor Yellow
        git push
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Pushed successfully" -ForegroundColor Green
        } else {
            Write-Warning "Push failed - changes are committed locally"
        }
    } else {
        Write-Error "Commit failed"
        exit 1
    }
} else {
    Write-Host "No changes to commit" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=== Done ==="
