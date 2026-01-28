# AI Idea Lab - Firebase/Cloud Run Deployment Guide

このガイドでは、AI Idea LabをGoogle Cloud Runにデプロイする手順を説明します。

## 📋 前提条件

1. **Google Cloud Platform アカウント**
   - プロジェクトを作成済み
   - 課金が有効化されている

2. **必要なツール**
   - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)

3. **APIキー**
   - OpenAI API Key (オプション)
   - Anthropic API Key (オプション)
   - Google AI API Key (オプション)

## 🚀 デプロイ手順

### 1. プロジェクトIDの設定

`.firebaserc` ファイルを編集して、あなたのGCPプロジェクトIDに変更してください:

```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

### 2. Google Cloud認証

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. デプロイ実行

**Windows (PowerShell):**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

このスクリプトは以下を自動的に実行します:
- 必要なGCP APIの有効化
- Secret Managerにプレースホルダーシークレットを作成
- Dockerコンテナのビルドとプッシュ
- Cloud Runへのデプロイ

### 4. APIキーの設定

**Windows (PowerShell):**
```powershell
.\update-secrets.ps1
```

**Linux/Mac:**
```bash
chmod +x update-secrets.sh
./update-secrets.sh
```

プロンプトに従って、各APIキーを入力してください。

### 5. 再デプロイ

APIキーを更新した後、変更を反映するために再デプロイします:

**Windows:**
```powershell
.\deploy.ps1
```

**Linux/Mac:**
```bash
./deploy.sh
```

## 🔍 デプロイの確認

デプロイが完了すると、サービスURLが表示されます:

```
✅ Deployment complete!
======================================
🌐 Service URL: https://ai-idea-lab-xxxxx-an.a.run.app
```

ブラウザでこのURLにアクセスして、アプリケーションが正常に動作していることを確認してください。

## 🔐 Secret Managerでのキー管理

### シークレットの確認

```bash
# シークレット一覧
gcloud secrets list

# 特定のシークレットのバージョン確認
gcloud secrets versions list OPENAI_API_KEY
```

### 手動でのシークレット更新

```bash
# OpenAI API Key
echo "sk-your-actual-key" | gcloud secrets versions add OPENAI_API_KEY --data-file=-

# Anthropic API Key
echo "sk-ant-your-actual-key" | gcloud secrets versions add ANTHROPIC_API_KEY --data-file=-

# Google AI API Key
echo "AIza-your-actual-key" | gcloud secrets versions add GOOGLE_API_KEY --data-file=-
```

## 📊 ログの確認

```bash
# リアルタイムログ
gcloud run services logs tail ai-idea-lab --region=asia-northeast1

# 過去のログ
gcloud run services logs read ai-idea-lab --region=asia-northeast1 --limit=50
```

## 💰 コスト管理

Cloud Runは使用した分だけ課金されます:

- **無料枠**: 月間200万リクエストまで無料
- **スケールtoゼロ**: 使用していない時は課金なし
- **推定コスト**: 月間1000セッション程度で $5-15/月

### コスト削減のヒント

```bash
# 最小インスタンス数を0に設定（デフォルト）
gcloud run services update ai-idea-lab --min-instances=0 --region=asia-northeast1

# 最大インスタンス数を制限
gcloud run services update ai-idea-lab --max-instances=5 --region=asia-northeast1
```

## 🔄 継続的デプロイ (CI/CD)

Cloud Buildを使用した自動デプロイを設定できます:

```bash
# Cloud Buildトリガーの作成
gcloud builds submit --config=cloudbuild.yaml
```

GitHubと連携して、プッシュ時に自動デプロイすることも可能です。

## 🛠️ トラブルシューティング

### デプロイが失敗する

```bash
# サービスの状態確認
gcloud run services describe ai-idea-lab --region=asia-northeast1

# 最新のログを確認
gcloud run services logs read ai-idea-lab --region=asia-northeast1 --limit=100
```

### APIキーが認識されない

1. Secret Managerでシークレットが正しく作成されているか確認
2. Cloud Runサービスにシークレットへのアクセス権限があるか確認
3. 再デプロイを実行

### Dockerビルドエラー

```bash
# ローカルでテスト
docker build -t ai-idea-lab-test .
docker run -p 8080:8080 ai-idea-lab-test
```

## 📞 サポート

問題が解決しない場合:
- [Cloud Run ドキュメント](https://cloud.google.com/run/docs)
- [Secret Manager ドキュメント](https://cloud.google.com/secret-manager/docs)
- [Streamlit ドキュメント](https://docs.streamlit.io/)

## 🔄 アップデート手順

コードを更新した後:

1. 変更をコミット
2. デプロイスクリプトを実行

```bash
# Windows
.\deploy.ps1

# Linux/Mac
./deploy.sh
```

Cloud Runは自動的に新しいバージョンにトラフィックを切り替えます。
