#!/bin/bash

# AI Idea Lab - Cloud Run Deployment Script
# This script deploys the Streamlit app to Google Cloud Run with Secret Manager integration

set -e

echo "🚀 AI Idea Lab - Cloud Run Deployment"
echo "======================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project selected"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Project: $PROJECT_ID"
echo ""

# Configuration
SERVICE_NAME="ai-idea-lab"
REGION="asia-northeast1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Step 1: Enable required APIs
echo "🔧 Step 1/5: Enabling required APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    secretmanager.googleapis.com \
    containerregistry.googleapis.com \
    --project=$PROJECT_ID

# Step 2: Create secrets in Secret Manager (if they don't exist)
echo ""
echo "🔐 Step 2/5: Setting up Secret Manager..."

create_secret_if_not_exists() {
    SECRET_NAME=$1
    if ! gcloud secrets describe $SECRET_NAME --project=$PROJECT_ID &>/dev/null; then
        echo "Creating secret: $SECRET_NAME"
        echo -n "placeholder-key-please-update" | gcloud secrets create $SECRET_NAME \
            --data-file=- \
            --replication-policy="automatic" \
            --project=$PROJECT_ID
        echo "⚠️  Please update $SECRET_NAME with your actual API key:"
        echo "   gcloud secrets versions add $SECRET_NAME --data-file=- <<< 'YOUR_ACTUAL_KEY'"
    else
        echo "✓ Secret $SECRET_NAME already exists"
    fi
}

create_secret_if_not_exists "OPENAI_API_KEY"
create_secret_if_not_exists "ANTHROPIC_API_KEY"
create_secret_if_not_exists "GOOGLE_API_KEY"

# Step 3: Build container
echo ""
echo "🏗️  Step 3/5: Building Docker container..."
docker build -t $IMAGE_NAME:latest .

# Step 4: Push to Container Registry
echo ""
echo "📤 Step 4/5: Pushing to Container Registry..."
docker push $IMAGE_NAME:latest

# Step 5: Deploy to Cloud Run
echo ""
echo "🚀 Step 5/5: Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image=$IMAGE_NAME:latest \
    --platform=managed \
    --region=$REGION \
    --allow-unauthenticated \
    --set-secrets=OPENAI_API_KEY=OPENAI_API_KEY:latest,ANTHROPIC_API_KEY=ANTHROPIC_API_KEY:latest,GOOGLE_API_KEY=GOOGLE_API_KEY:latest \
    --memory=2Gi \
    --cpu=2 \
    --max-instances=10 \
    --min-instances=0 \
    --timeout=300 \
    --project=$PROJECT_ID

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)' --project=$PROJECT_ID)

echo ""
echo "✅ Deployment complete!"
echo "======================================"
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "📝 Next steps:"
echo "1. Update your API keys in Secret Manager:"
echo "   gcloud secrets versions add OPENAI_API_KEY --data-file=- <<< 'sk-...'"
echo "   gcloud secrets versions add ANTHROPIC_API_KEY --data-file=- <<< 'sk-ant-...'"
echo "   gcloud secrets versions add GOOGLE_API_KEY --data-file=- <<< 'AIza...'"
echo ""
echo "2. After updating secrets, redeploy:"
echo "   ./deploy.sh"
echo ""
