# 💡 AI Idea Lab Pro

複数のAIが「Yes, And」の精神でアイデアを発展・エンハンスし、最高のアイデアを生み出す創造的コラボレーションアプリ。

## 🎯 コンセプト

従来のAIディベート（否定・反論）ではなく、**建設的な対話**によってアイデアを発展させます。

```
アイデア → 発展 → エンハンス → 統合 → より良いアイデア
```

## 🚀 セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. APIキーの設定

```bash
# テンプレートをコピー
cp .env.example .env

# .envを編集してAPIキーを設定
```

必要なAPIキー（使いたいモデルのみでOK）：
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys
- **Google AI**: https://aistudio.google.com/app/apikey

### 3. アプリの起動

```bash
streamlit run app.py
```

## 📦 利用可能なモデル

| OpenAI 🟢 | Anthropic 🟣 | Google 🔵 |
|-----------|--------------|-----------|
| GPT-5 | Claude Opus 4.5 | Gemini 2.5 Pro |
| GPT-4o | Claude Opus 4 | Gemini 2.5 Flash |
| o3 | Claude Sonnet 4 | Gemini 2.0 Flash |
| o4-mini | Claude Haiku 4.5 | Gemini 3 Pro (Preview) |
| GPT-4.1 | | Gemini 3 Flash (Preview) |

## 🎮 使い方

1. **コラボレーター選択**: 議論に参加するAIを2体以上選択
2. **ファシリテーター選択**: 最終まとめ役（議論には参加しない）
3. **テーマ入力**: アイデアを発展させたいテーマを入力
4. **セッション開始**: 🚀ボタンをクリック

## 📁 プロジェクト構成

```
ai-idea-lab/
├── .env.example     # 環境変数テンプレート
├── .env             # 環境変数（APIキー）※gitignore
├── .gitignore
├── README.md
├── requirements.txt
├── config.py        # 設定・モデル定義
└── app.py           # メインアプリ
```

## 🔧 カスタマイズ

### プロンプトの変更

`config.py` の以下を編集：
- `SYSTEM_PROMPT`: コラボレーターの振る舞い
- `FACILITATOR_PROMPT`: ファシリテーターの出力フォーマット

### モデルの追加

`config.py` の各モデル辞書に追加：
```python
OPENAI_MODELS = {
    "新モデル名": "model-id",
    ...
}
```

## 🚧 今後の拡張アイデア

- [ ] セッション履歴の保存・検索
- [ ] PDFレポート出力
- [ ] ユーザーが途中で意見を挟める機能
- [ ] Slack/Notion連携
- [ ] ストリーミング出力対応
- [ ] カスタムプロンプトのUI設定

## 📝 ライセンス

MIT License
