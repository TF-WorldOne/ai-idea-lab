# AI Idea Lab - Secret Manager Update Script (PowerShell)
# This script helps you update API keys in Google Secret Manager

$ErrorActionPreference = "Stop"

Write-Host "🔐 AI Idea Lab - Update API Keys" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Get project ID
$PROJECT_ID = (gcloud config get-value project 2>$null)
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "❌ Error: No GCP project selected" -ForegroundColor Red
    Write-Host "Run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Project: $PROJECT_ID" -ForegroundColor Green
Write-Host ""

# Function to update a secret
function Update-Secret {
    param($SecretName)
    
    Write-Host "Updating $SecretName..." -ForegroundColor Yellow
    $SecretValue = Read-Host "Enter your $SecretName (input will be hidden)" -AsSecureString
    
    # Convert SecureString to plain text
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecretValue)
    $PlainValue = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    if ([string]::IsNullOrEmpty($PlainValue)) {
        Write-Host "⚠️  Skipping $SecretName (empty value)" -ForegroundColor Yellow
        return
    }
    
    $PlainValue | gcloud secrets versions add $SecretName `
        --data-file=- `
        --project=$PROJECT_ID
    
    Write-Host "✅ $SecretName updated successfully" -ForegroundColor Green
    Write-Host ""
}

# Update secrets
Write-Host "Please enter your API keys (press Enter to skip):" -ForegroundColor Cyan
Write-Host ""

Update-Secret "OPENAI_API_KEY"
Update-Secret "ANTHROPIC_API_KEY"
Update-Secret "GOOGLE_API_KEY"

Write-Host "✅ All secrets updated!" -ForegroundColor Green
Write-Host ""
Write-Host "🔄 To apply changes, redeploy your service:" -ForegroundColor Yellow
Write-Host "   .\deploy.ps1" -ForegroundColor Gray
Write-Host ""
