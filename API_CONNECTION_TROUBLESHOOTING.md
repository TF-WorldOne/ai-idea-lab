# API接続エラーのトラブルシューティング

## 現在の状況

アプリは正常にデプロイされていますが、以下のエラーが発生しています：
- ❌ GPT-4o: Connection error
- ❌ Claude Sonnet 4: Connection error
- ⚠️ Gemini: `INTERNAL:Illegal header value`

## 原因

ログから判明した問題：
```
E0000 00:00:1769587697.588278 plugin_credentials.cc:79] validate_metadata_from_plugin: INTERNAL:Illegal header value
E0000 00:00:1769587697.588331 plugin_credentials.cc:82] Plugin added invalid metadata value.
```

これは、APIキーに以下のような問題がある可能性があります：
1. 改行文字が含まれている
2. 余分な空白が含まれている
3. APIキー自体が無効
4. APIキーの形式が間違っている

## 解決方法

### 1. APIキーを再確認

各APIキーが正しい形式であることを確認してください：

**OpenAI API Key:**
- 形式: `sk-proj-...` または `sk-...`
- 長さ: 約100-200文字
- 改行なし、空白なし

**Anthropic API Key:**
- 形式: `sk-ant-...`
- 改行なし、空白なし

**Google AI API Key:**
- 形式: `AIza...`
- 改行なし、空白なし

### 2. APIキーを再設定

以下のコマンドで、APIキーを1つずつクリーンに設定し直してください：

```powershell
# OpenAI API Key
$OPENAI_KEY = Read-Host "Enter OpenAI API Key (sk-proj-...)"
echo $OPENAI_KEY.Trim() | gcloud secrets versions add OPENAI_API_KEY --data-file=- --project=investment-analyst-b3e5c

# Anthropic API Key
$ANTHROPIC_KEY = Read-Host "Enter Anthropic API Key (sk-ant-...)"
echo $ANTHROPIC_KEY.Trim() | gcloud secrets versions add ANTHROPIC_API_KEY --data-file=- --project=investment-analyst-b3e5c

# Google AI API Key
$GOOGLE_KEY = Read-Host "Enter Google AI API Key (AIza...)"
echo $GOOGLE_KEY.Trim() | gcloud secrets versions add GOOGLE_API_KEY --data-file=- --project=investment-analyst-b3e5c
```

### 3. APIキーの有効性を確認

各プラットフォームで、APIキーが有効であることを確認してください：

**OpenAI:**
```powershell
$OPENAI_KEY = gcloud secrets versions access latest --secret=OPENAI_API_KEY --project=investment-analyst-b3e5c
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_KEY"
```

**Anthropic:**
```powershell
$ANTHROPIC_KEY = gcloud secrets versions access latest --secret=ANTHROPIC_API_KEY --project=investment-analyst-b3e5c
curl https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_KEY" -H "anthropic-version: 2023-06-01" -H "Content-Type: application/json" -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":10,"messages":[{"role":"user","content":"test"}]}'
```

**Google AI:**
```powershell
$GOOGLE_KEY = gcloud secrets versions access latest --secret=GOOGLE_API_KEY --project=investment-analyst-b3e5c
curl "https://generativelanguage.googleapis.com/v1/models?key=$GOOGLE_KEY"
```

### 4. 課金設定を確認

各APIプロバイダーで課金設定が有効になっているか確認してください：

- **OpenAI**: https://platform.openai.com/account/billing
- **Anthropic**: https://console.anthropic.com/settings/billing
- **Google AI**: https://console.cloud.google.com/billing

### 5. 再デプロイ

APIキーを更新した後、サービスを再起動してください：

```powershell
gcloud run services update ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c
```

または、完全に再デプロイ：

```powershell
.\deploy.ps1
```

## よくある問題

### 問題: "Connection error"
**原因**: APIキーが無効、または課金設定が無効
**解決**: APIキーと課金設定を確認

### 問題: "Illegal header value"
**原因**: APIキーに改行や特殊文字が含まれている
**解決**: `.Trim()`を使ってクリーンなAPIキーを設定

### 問題: "Rate limit exceeded"
**原因**: API使用量制限に達している
**解決**: 使用量を確認し、制限を増やすか時間を置く

## 確認コマンド

```powershell
# Secret Managerの値を確認（改行や空白をチェック）
gcloud secrets versions access latest --secret=OPENAI_API_KEY --project=investment-analyst-b3e5c | Format-Hex
gcloud secrets versions access latest --secret=ANTHROPIC_API_KEY --project=investment-analyst-b3e5c | Format-Hex
gcloud secrets versions access latest --secret=GOOGLE_API_KEY --project=investment-analyst-b3e5c | Format-Hex

# Cloud Runの環境変数設定を確認
gcloud run services describe ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c --format="value(spec.template.spec.containers[0].env)"

# ログをリアルタイムで確認
gcloud run services logs tail ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c
```
