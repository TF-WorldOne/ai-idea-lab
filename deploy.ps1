# AI Idea Lab - Cloud Run Deployment Script (PowerShell)
# This script deploys the Streamlit app to Google Cloud Run with Secret Manager integration

$ErrorActionPreference = "Stop"

Write-Host "🚀 AI Idea Lab - Cloud Run Deployment" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if gcloud is installed
try {
    $null = Get-Command gcloud -ErrorAction Stop
} catch {
    Write-Host "❌ Error: gcloud CLI is not installed" -ForegroundColor Red
    Write-Host "Please install it from: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    exit 1
}

# Get project ID
$PROJECT_ID = (gcloud config get-value project 2>$null)
if ([string]::IsNullOrEmpty($PROJECT_ID)) {
    Write-Host "❌ Error: No GCP project selected" -ForegroundColor Red
    Write-Host "Run: gcloud config set project YOUR_PROJECT_ID" -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Project: $PROJECT_ID" -ForegroundColor Green
Write-Host ""

# Configuration
$SERVICE_NAME = "ai-idea-lab"
$REGION = "asia-northeast1"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Step 1: Enable required APIs
Write-Host "🔧 Step 1/5: Enabling required APIs..." -ForegroundColor Yellow
gcloud services enable `
    run.googleapis.com `
    cloudbuild.googleapis.com `
    secretmanager.googleapis.com `
    containerregistry.googleapis.com `
    --project=$PROJECT_ID

# Step 2: Create secrets in Secret Manager (if they don't exist)
Write-Host ""
Write-Host "🔐 Step 2/5: Setting up Secret Manager..." -ForegroundColor Yellow

function Create-SecretIfNotExists {
    param($SecretName)
    
    $secretExists = gcloud secrets describe $SecretName --project=$PROJECT_ID 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Creating secret: $SecretName" -ForegroundColor Cyan
        "placeholder-key-please-update" | gcloud secrets create $SecretName `
            --data-file=- `
            --replication-policy="automatic" `
            --project=$PROJECT_ID
        Write-Host "⚠️  Please update $SecretName with your actual API key:" -ForegroundColor Yellow
        Write-Host "   .\update-secrets.ps1" -ForegroundColor Gray
    } else {
        Write-Host "✓ Secret $SecretName already exists" -ForegroundColor Green
    }
}

Create-SecretIfNotExists "OPENAI_API_KEY"
Create-SecretIfNotExists "ANTHROPIC_API_KEY"
Create-SecretIfNotExists "GOOGLE_API_KEY"

# Step 3: Build container
Write-Host ""
Write-Host "🏗️  Step 3/5: Building Docker container..." -ForegroundColor Yellow
docker build -t ${IMAGE_NAME}:latest .

# Step 4: Push to Container Registry
Write-Host ""
Write-Host "📤 Step 4/5: Pushing to Container Registry..." -ForegroundColor Yellow
docker push ${IMAGE_NAME}:latest

# Step 5: Deploy to Cloud Run
Write-Host ""
Write-Host "🚀 Step 5/5: Deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME `
    --image=${IMAGE_NAME}:latest `
    --platform=managed `
    --region=$REGION `
    --allow-unauthenticated `
    --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest,ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest `
    --memory=2Gi `
    --cpu=2 `
    --max-instances=10 `
    --min-instances=0 `
    --timeout=300 `
    --project=$PROJECT_ID

# Get the service URL
$SERVICE_URL = (gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)' --project=$PROJECT_ID)

Write-Host ""
Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🌐 Service URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "1. Update your API keys in Secret Manager:" -ForegroundColor White
Write-Host "   .\update-secrets.ps1" -ForegroundColor Gray
Write-Host ""
Write-Host "2. After updating secrets, redeploy:" -ForegroundColor White
Write-Host "   .\deploy.ps1" -ForegroundColor Gray
Write-Host ""
