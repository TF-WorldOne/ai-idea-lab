# AI Idea Lab - セットアップチェックリスト

このチェックリストを使用して、デプロイ前に必要なツールがインストールされているか確認してください。

## ✅ 必須ツールのインストール確認

### 1. Google Cloud SDK

**確認コマンド:**
```powershell
gcloud --version
```

**インストールされていない場合:**
1. [Google Cloud SDK インストーラー](https://cloud.google.com/sdk/docs/install)をダウンロード
2. インストーラーを実行
3. インストール後、PowerShellを再起動
4. 認証を実行:
   ```powershell
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

### 2. Docker Desktop

**確認コマンド:**
```powershell
docker --version
```

**インストールされていない場合:**
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)をダウンロード
2. インストーラーを実行
3. インストール後、PCを再起動
4. Docker Desktopを起動して、動作確認

### 3. Git (オプション - ソース管理用)

**確認コマンド:**
```powershell
git --version
```

**インストールされていない場合:**
1. [Git for Windows](https://git-scm.com/download/win)をダウンロード
2. インストーラーを実行

## 🔧 GCPプロジェクトの設定

### 1. プロジェクトの作成

1. [Google Cloud Console](https://console.cloud.google.com/)にアクセス
2. 新しいプロジェクトを作成
3. プロジェクトIDをメモ

### 2. 課金の有効化

1. プロジェクトで課金を有効化
2. 無料トライアルクレジット($300)を利用可能

### 3. プロジェクトIDの設定

`.firebaserc` ファイルを編集:
```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

## 🔑 APIキーの準備

デプロイ後に必要になるため、事前に取得しておくことを推奨します:

### OpenAI API Key (オプション)
- [OpenAI Platform](https://platform.openai.com/api-keys)
- 形式: `sk-...`

### Anthropic API Key (オプション)
- [Anthropic Console](https://console.anthropic.com/settings/keys)
- 形式: `sk-ant-...`

### Google AI API Key (オプション)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- 形式: `AIza...`

## 📋 デプロイ前チェックリスト

- [ ] Google Cloud SDKがインストールされている
- [ ] Docker Desktopがインストールされ、起動している
- [ ] GCPプロジェクトが作成されている
- [ ] 課金が有効化されている
- [ ] `.firebaserc`にプロジェクトIDが設定されている
- [ ] APIキーを準備している（最低1つ）
- [ ] `gcloud auth login`で認証済み
- [ ] `gcloud config set project`でプロジェクトを設定済み

## 🚀 次のステップ

すべてのチェックが完了したら、デプロイを実行できます:

```powershell
.\deploy.ps1
```

詳細な手順は `DEPLOYMENT.md` を参照してください。

## ❓ トラブルシューティング

### Docker Desktopが起動しない

- WSL 2が有効になっているか確認
- Hyper-Vが有効になっているか確認（Windows Pro/Enterprise）
- BIOSで仮想化が有効になっているか確認

### gcloudコマンドが認識されない

- PowerShellを再起動
- 環境変数PATHにGoogle Cloud SDKが追加されているか確認
- インストールディレクトリ: `C:\Users\[USERNAME]\AppData\Local\Google\Cloud SDK\google-cloud-sdk\bin`

### プロジェクトIDがわからない

```powershell
gcloud projects list
```

現在設定されているプロジェクトを確認:
```powershell
gcloud config get-value project
```
