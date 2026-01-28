# AI Idea Lab - インストールスクリプト
# Docker DesktopとGoogle Cloud SDKを自動インストール

$ErrorActionPreference = "Stop"

Write-Host "🚀 AI Idea Lab - 必須ツールのインストール" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 管理者権限チェック
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "⚠️  このスクリプトは管理者権限で実行することを推奨します" -ForegroundColor Yellow
    Write-Host "   右クリック → '管理者として実行' で再実行してください" -ForegroundColor Yellow
    Write-Host ""
    $continue = Read-Host "続行しますか? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 0
    }
}

# Step 1: Docker Desktopのダウンロード
Write-Host "📦 Step 1/4: Docker Desktopをダウンロード中..." -ForegroundColor Yellow
$dockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
$dockerInstaller = "$env:TEMP\DockerDesktopInstaller.exe"

if (Test-Path $dockerInstaller) {
    Write-Host "✓ Docker Desktopインストーラーは既にダウンロード済みです" -ForegroundColor Green
} else {
    try {
        Write-Host "  ダウンロード中... (約600MB、数分かかる場合があります)" -ForegroundColor Gray
        Invoke-WebRequest -Uri $dockerUrl -OutFile $dockerInstaller -UseBasicParsing
        Write-Host "✓ Docker Desktopのダウンロード完了" -ForegroundColor Green
    } catch {
        Write-Host "❌ Docker Desktopのダウンロードに失敗しました" -ForegroundColor Red
        Write-Host "   手動でダウンロードしてください: $dockerUrl" -ForegroundColor Yellow
        $dockerInstaller = $null
    }
}

# Step 2: Google Cloud SDKのダウンロード
Write-Host ""
Write-Host "📦 Step 2/4: Google Cloud SDKをダウンロード中..." -ForegroundColor Yellow
$gcloudUrl = "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe"
$gcloudInstaller = "$env:TEMP\GoogleCloudSDKInstaller.exe"

if (Test-Path $gcloudInstaller) {
    Write-Host "✓ Google Cloud SDKインストーラーは既にダウンロード済みです" -ForegroundColor Green
} else {
    try {
        Write-Host "  ダウンロード中... (約100MB)" -ForegroundColor Gray
        Invoke-WebRequest -Uri $gcloudUrl -OutFile $gcloudInstaller -UseBasicParsing
        Write-Host "✓ Google Cloud SDKのダウンロード完了" -ForegroundColor Green
    } catch {
        Write-Host "❌ Google Cloud SDKのダウンロードに失敗しました" -ForegroundColor Red
        Write-Host "   手動でダウンロードしてください: $gcloudUrl" -ForegroundColor Yellow
        $gcloudInstaller = $null
    }
}

# Step 3: Docker Desktopのインストール
Write-Host ""
Write-Host "🔧 Step 3/4: Docker Desktopをインストール中..." -ForegroundColor Yellow
if ($dockerInstaller -and (Test-Path $dockerInstaller)) {
    Write-Host "  インストーラーを起動します..." -ForegroundColor Gray
    Write-Host "  ⚠️  インストールウィザードの指示に従ってください" -ForegroundColor Yellow
    Write-Host "  ⚠️  インストール後、PCの再起動が必要な場合があります" -ForegroundColor Yellow
    Start-Process -FilePath $dockerInstaller -Wait
    Write-Host "✓ Docker Desktopのインストール完了" -ForegroundColor Green
} else {
    Write-Host "⚠️  Docker Desktopインストーラーが見つかりません" -ForegroundColor Yellow
    Write-Host "   手動でインストールしてください: https://www.docker.com/products/docker-desktop" -ForegroundColor Gray
}

# Step 4: Google Cloud SDKのインストール
Write-Host ""
Write-Host "🔧 Step 4/4: Google Cloud SDKをインストール中..." -ForegroundColor Yellow
if ($gcloudInstaller -and (Test-Path $gcloudInstaller)) {
    Write-Host "  インストーラーを起動します..." -ForegroundColor Gray
    Write-Host "  ⚠️  インストールウィザードの指示に従ってください" -ForegroundColor Yellow
    Start-Process -FilePath $gcloudInstaller -Wait
    Write-Host "✓ Google Cloud SDKのインストール完了" -ForegroundColor Green
} else {
    Write-Host "⚠️  Google Cloud SDKインストーラーが見つかりません" -ForegroundColor Yellow
    Write-Host "   手動でインストールしてください: https://cloud.google.com/sdk/docs/install" -ForegroundColor Gray
}

# 完了メッセージ
Write-Host ""
Write-Host "✅ インストールプロセス完了!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 次のステップ:" -ForegroundColor Yellow
Write-Host "1. PowerShellを再起動してください" -ForegroundColor White
Write-Host "2. Docker Desktopを起動してください" -ForegroundColor White
Write-Host "3. 以下のコマンドでインストールを確認:" -ForegroundColor White
Write-Host "   docker --version" -ForegroundColor Gray
Write-Host "   gcloud --version" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Google Cloudにログイン:" -ForegroundColor White
Write-Host "   gcloud auth login" -ForegroundColor Gray
Write-Host "   gcloud config set project investment-analyst-b3e5c" -ForegroundColor Gray
Write-Host ""
Write-Host "5. デプロイを実行:" -ForegroundColor White
Write-Host "   .\deploy.ps1" -ForegroundColor Gray
Write-Host ""
