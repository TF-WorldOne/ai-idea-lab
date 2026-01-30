@echo off
echo ========================================================
echo  AI Idea Lab Pro - Cloud Run Deployment
echo  Project: investment-analyst-b3e5c
echo ========================================================

echo.
echo [1/2] Building Container Image with Artifact Registry...
call gcloud builds submit --tag asia-northeast1-docker.pkg.dev/investment-analyst-b3e5c/ai-idea-lab/ai-idea-lab --region=asia-northeast1 --project investment-analyst-b3e5c .
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Deploying to Cloud Run...
call gcloud run deploy ai-idea-lab ^
  --image asia-northeast1-docker.pkg.dev/investment-analyst-b3e5c/ai-idea-lab/ai-idea-lab ^
  --platform managed ^
  --region asia-northeast1 ^
  --allow-unauthenticated ^
  --port 8080 ^
  --project investment-analyst-b3e5c
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [SUCCESS] Build and Deployment Complete!
echo Check the URL above or visit:
echo https://ai-idea-lab-1b89461983457.asia-northeast1.run.app
pause
