# APIキーの設定方法

## 必要なAPIキー

AI Idea Labを使用するには、以下の3つのAPIキーが必要です：

### 1. OpenAI API Key
- **用途**: GPT-4, GPT-3.5などのOpenAIモデル
- **取得方法**: https://platform.openai.com/api-keys
  1. OpenAIアカウントにログイン
  2. 左メニューから「API keys」を選択
  3. 「Create new secret key」をクリック
  4. キーをコピー（一度しか表示されません）

### 2. Anthropic API Key
- **用途**: Claude 3.5 Sonnet, Claude 3 Opusなどのモデル
- **取得方法**: https://console.anthropic.com/settings/keys
  1. Anthropicアカウントにログイン
  2. 「API Keys」セクションに移動
  3. 「Create Key」をクリック
  4. キーをコピー

### 3. Google AI API Key
- **用途**: Gemini Pro, Gemini Flashなどのモデル
- **取得方法**: https://makersuite.google.com/app/apikey
  1. Googleアカウントでログイン
  2. 「Get API key」をクリック
  3. 「Create API key in new project」または既存プロジェクトを選択
  4. キーをコピー

## APIキーの登録手順

### 方法1: 自動スクリプト（推奨）

PowerShellで以下のコマンドを実行：

```powershell
cd c:\Antigravity-Workspace\X-Think\ai-idea-lab
.\update-secrets.ps1
```

スクリプトが起動したら：
1. OpenAI API Keyを入力してEnter
2. Anthropic API Keyを入力してEnter
3. Google AI API Keyを入力してEnter

### 方法2: 手動コマンド

各APIキーを個別に設定する場合：

```powershell
# OpenAI API Key
echo "YOUR_OPENAI_API_KEY" | gcloud secrets versions add OPENAI_API_KEY --data-file=- --project=investment-analyst-b3e5c

# Anthropic API Key
echo "YOUR_ANTHROPIC_API_KEY" | gcloud secrets versions add ANTHROPIC_API_KEY --data-file=- --project=investment-analyst-b3e5c

# Google AI API Key
echo "YOUR_GOOGLE_API_KEY" | gcloud secrets versions add GOOGLE_API_KEY --data-file=- --project=investment-analyst-b3e5c
```

**注意**: `YOUR_OPENAI_API_KEY`などを実際のAPIキーに置き換えてください。

## 確認方法

APIキーが正しく設定されたか確認：

```powershell
# シークレットのバージョンを確認
gcloud secrets versions list OPENAI_API_KEY --project=investment-analyst-b3e5c
gcloud secrets versions list ANTHROPIC_API_KEY --project=investment-analyst-b3e5c
gcloud secrets versions list GOOGLE_API_KEY --project=investment-analyst-b3e5c
```

最新バージョン（version 2）が表示されればOKです。

## アプリケーションのテスト

1. デプロイされたアプリにアクセス:
   https://ai-idea-lab-1089461983457.asia-northeast1.run.app

2. トピックを入力（例: "新しいモバイルアプリのアイデア"）

3. 使用するAIモデルを選択

4. 「ディスカッション開始」をクリック

5. 各AIモデルが正常に応答すれば成功です！

## トラブルシューティング

### エラー: "API key not found"
- Secret Managerにキーが正しく登録されているか確認
- Cloud Runサービスを再デプロイ: `.\deploy.ps1`

### エラー: "Invalid API key"
- APIキーが正しいか確認
- APIキーの有効期限が切れていないか確認
- 各プラットフォームで課金設定が有効か確認

### エラー: "Rate limit exceeded"
- APIの使用量制限に達している可能性
- 各プラットフォームのダッシュボードで使用状況を確認

## セキュリティのベストプラクティス

✅ **DO**:
- APIキーは絶対にGitにコミットしない
- Secret Managerを使用して安全に管理
- 定期的にキーをローテーション

❌ **DON'T**:
- APIキーをコードに直接書かない
- 公開リポジトリにAPIキーを含めない
- APIキーをSlackやメールで共有しない

## コスト管理

各APIプロバイダーで使用量制限を設定することをお勧めします：

- **OpenAI**: https://platform.openai.com/account/billing/limits
- **Anthropic**: https://console.anthropic.com/settings/limits
- **Google AI**: https://console.cloud.google.com/apis/api/generativelanguage.googleapis.com/quotas

## サポート

問題が発生した場合：
1. `DEPLOYMENT.md`のトラブルシューティングセクションを確認
2. Cloud Runのログを確認: `gcloud run logs read ai-idea-lab --region=asia-northeast1`
