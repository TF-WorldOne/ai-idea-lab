# 403 Forbiddenエラーの解決方法

## 問題

Cloud Runサービスにアクセスすると「Error: Forbidden」が表示されます。
これは、GCP組織ポリシーによって公開アクセス（`allUsers`）が制限されているためです。

## 解決方法

### オプション1: GCPコンソールで手動設定（推奨）

1. **Cloud Runコンソールを開く**
   https://console.cloud.google.com/run?project=investment-analyst-b3e5c

2. **サービスを選択**
   - `ai-idea-lab` サービスをクリック

3. **権限タブを開く**
   - 上部の「権限」タブをクリック

4. **プリンシパルを追加**
   - 「プリンシパルを追加」ボタンをクリック
   - 新しいプリンシパル: `allUsers`
   - ロール: `Cloud Run 起動元`
   - 「保存」をクリック

5. **確認**
   - ブラウザでアプリURLを再読み込み
   - https://ai-idea-lab-1089461983457.asia-northeast1.run.app

### オプション2: 認証付きアクセス

公開アクセスが許可されない場合、認証付きでアクセスできます：

```powershell
# 認証トークンを取得してアクセス
$TOKEN = gcloud auth print-identity-token
curl -H "Authorization: Bearer $TOKEN" https://ai-idea-lab-1089461983457.asia-northeast1.run.app
```

### オプション3: 組織ポリシーの確認

組織管理者に連絡して、以下のポリシーを確認してもらってください：

```
constraints/iam.allowedPolicyMemberDomains
```

このポリシーが `allUsers` をブロックしている可能性があります。

## 手順の詳細（GCPコンソール）

### ステップバイステップ

1. **ブラウザで開く**
   ```
   https://console.cloud.google.com/run/detail/asia-northeast1/ai-idea-lab/permissions?project=investment-analyst-b3e5c
   ```

2. **「プリンシパルを追加」をクリック**

3. **以下を入力**
   - 新しいプリンシパル: `allUsers`
   - ロールを選択: `Cloud Run 起動元` (roles/run.invoker)

4. **「保存」をクリック**

5. **数秒待ってからアプリにアクセス**

## 確認方法

設定が正しく適用されたか確認：

```powershell
# IAMポリシーを確認
gcloud run services get-iam-policy ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c
```

以下のような出力があればOK：
```yaml
bindings:
- members:
  - allUsers
  role: roles/run.invoker
```

## トラブルシューティング

### それでもアクセスできない場合

1. **キャッシュをクリア**
   - ブラウザのキャッシュをクリアして再読み込み
   - シークレットモードで試す

2. **サービスの状態を確認**
   ```powershell
   gcloud run services describe ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c
   ```

3. **ログを確認**
   ```powershell
   gcloud run logs read ai-idea-lab --region=asia-northeast1 --project=investment-analyst-b3e5c --limit=50
   ```

## 代替案: Firebase Hostingを使用

Firebase Hostingを通じてアクセスすることもできます（追加設定が必要）：

```powershell
firebase deploy --only hosting
```

これにより、Firebaseドメインでアクセス可能になります。
