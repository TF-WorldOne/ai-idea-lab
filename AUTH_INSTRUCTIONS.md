# Google Cloud 認証手順

## 認証URLにアクセス

以下のURLをブラウザで開いてください:

https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=32555940559.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fsdk.cloud.google.com%2Fauthcode.html&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fappengine.admin+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcompute+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Faccounts.reauth&state=PlzVzMCojDKvGUUOn1ATZXpPFTkN7U&prompt=consent&token_usage=remote&access_type=offline&code_challenge=7DRsePfJnKsm0TFfVbqW-6q31Pfh00-_reXDuaVrWOk&code_challenge_method=S256

## 手順

1. 上記URLをブラウザで開く
2. Googleアカウントでログイン
3. 権限の許可を確認
4. 表示される認証コードをコピー
5. PowerShellに戻って認証コードを入力

## 認証コードの入力

PowerShellのプロンプトに認証コードを貼り付けてEnterを押してください。
