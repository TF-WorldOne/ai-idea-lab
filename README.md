# 🚀 AI Idea Lab - Quick Start Guide

## 📌 概要

AI Idea Labは、複数のAIモデルが協力してアイデアを発展させる創造的コラボレーションアプリです。

## 🎯 2つの実行方法

### 方法1: ローカル実行（開発・テスト用）

**必要なもの:**
- Python 3.11以上
- APIキー（OpenAI/Anthropic/Google AI のいずれか1つ以上）

**手順:**

1. **依存関係のインストール**
   ```bash
   pip install -r requirements.txt
   ```

2. **環境変数の設定**
   ```bash
   # .env.exampleをコピー
   copy .env.example .env
   
   # .envを編集してAPIキーを設定
   ```

3. **アプリの起動**
   ```bash
   streamlit run app.py
   ```

4. **ブラウザでアクセス**
   - 自動的に開かない場合: http://localhost:8501

---

### 方法2: Cloud Run デプロイ（本番環境）

**必要なもの:**
- Google Cloud Platform アカウント
- Docker Desktop
- Google Cloud SDK

**手順:**

1. **セットアップ確認**
   - `SETUP.md` を参照して必要なツールをインストール

2. **プロジェクトID設定**
   - `.firebaserc` を編集して実際のプロジェクトIDに変更

3. **デプロイ実行**
   ```powershell
   .\deploy.ps1
   ```

4. **APIキー設定**
   ```powershell
   .\update-secrets.ps1
   ```

5. **再デプロイ**
   ```powershell
   .\deploy.ps1
   ```

詳細は `DEPLOYMENT.md` を参照してください。

---

## 🎮 使い方

1. **サイドバーでAIを選択**
   - コラボレーター: 議論に参加するAI（2体以上）
   - ファシリテーター: 最終まとめ役（1体）

2. **テーマを入力**
   - アイデアを発展させたいトピックを記入

3. **セッション開始**
   - 「✦ Start Session」ボタンをクリック

4. **結果を確認**
   - 左側: AIの議論プロセス
   - 右側: 統合されたアイデアレポート

---

## 📁 ファイル構成

```
ai-idea-lab/
├── app.py                 # メインアプリケーション
├── config.py              # 設定・モデル定義
├── requirements.txt       # Python依存関係
├── .env.example           # 環境変数テンプレート
├── Dockerfile             # Cloud Run用コンテナ設定
├── deploy.ps1             # Windows用デプロイスクリプト
├── deploy.sh              # Linux/Mac用デプロイスクリプト
├── update-secrets.ps1     # APIキー更新（Windows）
├── update-secrets.sh      # APIキー更新（Linux/Mac）
├── SETUP.md               # セットアップガイド
├── DEPLOYMENT.md          # デプロイガイド
└── README.md              # このファイル
```

---

## 🔑 APIキーの取得

### OpenAI
- https://platform.openai.com/api-keys
- 利用可能モデル: GPT-5, GPT-4o, o3, o4-mini, GPT-4.1

### Anthropic
- https://console.anthropic.com/settings/keys
- 利用可能モデル: Claude Opus 4.5, Claude Opus 4, Claude Sonnet 4, Claude Haiku 4.5

### Google AI
- https://aistudio.google.com/app/apikey
- 利用可能モデル: Gemini 2.5 Pro, Gemini 2.5 Flash, Gemini 2.0 Flash, Gemini 3 Pro/Flash (Preview)

---

## 💡 使用例

### ビジネスアイデアの発展
```
テーマ: 地方創生のための新しいビジネスモデル
→ 複数のAIが異なる視点から提案
→ 統合された実行可能なプランを生成
```

### 技術的課題の解決
```
テーマ: スケーラブルなマイクロサービスアーキテクチャの設計
→ 各AIが専門的な観点から議論
→ ベストプラクティスを統合した設計案を出力
```

### クリエイティブな企画
```
テーマ: 次世代のSNSプラットフォームのコンセプト
→ 革新的なアイデアを多角的に発展
→ 具体的な実装ステップを含む企画書を生成
```

---

## ⚙️ カスタマイズ

### プロンプトの変更

`config.py` を編集:
- `SYSTEM_PROMPT`: AIコラボレーターの振る舞い
- `FACILITATOR_PROMPT`: ファシリテーターの出力形式

### モデルの追加

`config.py` の各モデル辞書に追加:
```python
OPENAI_MODELS = {
    "新モデル名": "model-id",
    ...
}
```

### 専門性レベルの調整

サイドバーの「Expertise Level」で調整:
- **Beginner**: 初心者向けの平易な説明
- **General**: 一般的な理解レベル
- **Professional**: 専門家向けの詳細な議論
- **Expert**: 最先端の技術的な深掘り

---

## 📊 コスト目安

### ローカル実行
- 費用: APIキーの使用料のみ
- 目安: 1セッション $0.01-0.10（モデルと長さによる）

### Cloud Run デプロイ
- 無料枠: 月間200万リクエストまで
- 推定: 月間1000セッションで $5-15
- スケールtoゼロ: 未使用時は課金なし

---

## 🛠️ トラブルシューティング

### ローカル実行でエラー

```bash
# 依存関係を再インストール
pip install --upgrade -r requirements.txt

# キャッシュをクリア
streamlit cache clear
```

### APIキーが認識されない

1. `.env` ファイルが正しい場所にあるか確認
2. APIキーの形式が正しいか確認
3. アプリを再起動

### Cloud Runデプロイエラー

`DEPLOYMENT.md` のトラブルシューティングセクションを参照

---

## 📞 サポート・リソース

- **Streamlit**: https://docs.streamlit.io/
- **Cloud Run**: https://cloud.google.com/run/docs
- **OpenAI**: https://platform.openai.com/docs
- **Anthropic**: https://docs.anthropic.com/
- **Google AI**: https://ai.google.dev/docs

---

## 📝 ライセンス

MIT License

---

## 🎉 今後の拡張予定

- [ ] セッション履歴の保存・検索
- [ ] PDFレポート出力
- [ ] ユーザーが途中で意見を挟める機能
- [ ] Slack/Notion連携
- [ ] ストリーミング出力対応
- [ ] カスタムプロンプトのUI設定
- [ ] マルチモーダル対応（画像・音声）
