# AI Idea Lab - 高速インストールスクリプト (winget使用)
# Windows Package Managerを使用した自動インストール

$ErrorActionPreference = "Stop"

Write-Host "🚀 AI Idea Lab - 高速ツールインストール" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# wingetの確認
Write-Host "🔍 Windows Package Managerを確認中..." -ForegroundColor Yellow
try {
    $wingetVersion = winget --version
    Write-Host "✓ winget バージョン: $wingetVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ wingetが見つかりません" -ForegroundColor Red
    Write-Host "   Windows 10 (1809以降) または Windows 11 が必要です" -ForegroundColor Yellow
    Write-Host "   Microsoft Storeから 'App Installer' をインストールしてください" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   代わりに install-tools.ps1 を使用してください" -ForegroundColor Gray
    exit 1
}

Write-Host ""

# Docker Desktopのインストール
Write-Host "🐳 Step 1/2: Docker Desktopをインストール中..." -ForegroundColor Yellow
Write-Host "   これには数分かかる場合があります..." -ForegroundColor Gray

try {
    # 既にインストールされているか確認
    $dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
    if ($dockerInstalled) {
        Write-Host "✓ Docker Desktopは既にインストールされています" -ForegroundColor Green
        docker --version
    } else {
        Write-Host "   wingetでDocker Desktopをインストール中..." -ForegroundColor Gray
        winget install -e --id Docker.DockerDesktop --accept-source-agreements --accept-package-agreements
        Write-Host "✓ Docker Desktopのインストール完了" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Docker Desktopの自動インストールに失敗しました" -ForegroundColor Yellow
    Write-Host "   手動でインストールしてください: https://www.docker.com/products/docker-desktop" -ForegroundColor Gray
}

Write-Host ""

# Google Cloud SDKのインストール
Write-Host "☁️  Step 2/2: Google Cloud SDKをインストール中..." -ForegroundColor Yellow
Write-Host "   これには数分かかる場合があります..." -ForegroundColor Gray

try {
    # 既にインストールされているか確認
    $gcloudInstalled = Get-Command gcloud -ErrorAction SilentlyContinue
    if ($gcloudInstalled) {
        Write-Host "✓ Google Cloud SDKは既にインストールされています" -ForegroundColor Green
        gcloud --version
    } else {
        Write-Host "   wingetでGoogle Cloud SDKをインストール中..." -ForegroundColor Gray
        winget install -e --id Google.CloudSDK --accept-source-agreements --accept-package-agreements
        Write-Host "✓ Google Cloud SDKのインストール完了" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠️  Google Cloud SDKの自動インストールに失敗しました" -ForegroundColor Yellow
    Write-Host "   手動でインストールしてください: https://cloud.google.com/sdk/docs/install" -ForegroundColor Gray
}

# 完了メッセージ
Write-Host ""
Write-Host "✅ インストール完了!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  重要: 以下の手順を実行してください" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. PowerShellを再起動してください（必須）" -ForegroundColor White
Write-Host "   新しいPowerShellウィンドウを開いてください" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Docker Desktopを起動してください" -ForegroundColor White
Write-Host "   スタートメニューから 'Docker Desktop' を検索して起動" -ForegroundColor Gray
Write-Host ""
Write-Host "3. インストールを確認:" -ForegroundColor White
Write-Host "   docker --version" -ForegroundColor Gray
Write-Host "   gcloud --version" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Google Cloudにログイン:" -ForegroundColor White
Write-Host "   gcloud auth login" -ForegroundColor Gray
Write-Host "   gcloud config set project investment-analyst-b3e5c" -ForegroundColor Gray
Write-Host ""
Write-Host "5. デプロイを実行:" -ForegroundColor White
Write-Host "   cd c:\Antigravity-Workspace\X-Think\ai-idea-lab" -ForegroundColor Gray
Write-Host "   .\deploy.ps1" -ForegroundColor Gray
Write-Host ""
