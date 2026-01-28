#!/bin/bash

# AI Idea Lab - Secret Manager Update Script
# This script helps you update API keys in Google Secret Manager

set -e

echo "🔐 AI Idea Lab - Update API Keys"
echo "================================="

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP project selected"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Project: $PROJECT_ID"
echo ""

# Function to update a secret
update_secret() {
    SECRET_NAME=$1
    echo "Updating $SECRET_NAME..."
    echo -n "Enter your $SECRET_NAME (input will be hidden): "
    read -s SECRET_VALUE
    echo ""
    
    if [ -z "$SECRET_VALUE" ]; then
        echo "⚠️  Skipping $SECRET_NAME (empty value)"
        return
    fi
    
    echo -n "$SECRET_VALUE" | gcloud secrets versions add $SECRET_NAME \
        --data-file=- \
        --project=$PROJECT_ID
    
    echo "✅ $SECRET_NAME updated successfully"
    echo ""
}

# Update secrets
echo "Please enter your API keys (press Enter to skip):"
echo ""

update_secret "OPENAI_API_KEY"
update_secret "ANTHROPIC_API_KEY"
update_secret "GOOGLE_API_KEY"

echo "✅ All secrets updated!"
echo ""
echo "🔄 To apply changes, redeploy your service:"
echo "   ./deploy.sh"
echo ""
