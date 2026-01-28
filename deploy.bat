@echo off
echo ========================================================
echo  AI Idea Lab Pro - Cloud Run Deployment
echo  Project: xworld-official
echo ========================================================

echo.
echo [1/2] Building Container Image (Cloud Build)...
call gcloud builds submit --tag gcr.io/xworld-official/ai-idea-lab-pro .
if %errorlevel% neq 0 (
    echo [ERROR] Build failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [2/2] Deploying to Cloud Run...
call gcloud run deploy ai-idea-lab-pro ^
  --image gcr.io/xworld-official/ai-idea-lab-pro ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --port 8080
if %errorlevel% neq 0 (
    echo [ERROR] Deployment failed.
    pause
    exit /b %errorlevel%
)

echo.
echo [SUCCESS] Deployment Complete!
echo check the URL above.
