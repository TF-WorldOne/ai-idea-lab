"""
AI Idea Lab - 設定管理モジュール
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込み（既存の環境変数を上書き）
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)


def _get_api_key(key_name: str) -> str:
    """APIキーを取得（Streamlit Cloud対応）"""
    # まずStreamlit Secretsを試す
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    # 次に環境変数を試す
    return os.getenv(key_name, "")


# --- API Keys ---
OPENAI_API_KEY = _get_api_key("OPENAI_API_KEY")
ANTHROPIC_API_KEY = _get_api_key("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = _get_api_key("GOOGLE_API_KEY")

# --- モデル定義 ---
# temperatureをサポートしないモデル
NO_TEMPERATURE_MODELS = {"gpt-5", "o3", "o4-mini"}

OPENAI_MODELS = {
    "GPT-5": "gpt-5",
    "GPT-4o": "gpt-4o",
    "o3": "o3",
    "o4-mini": "o4-mini",
    "GPT-4.1": "gpt-4.1",
}

ANTHROPIC_MODELS = {
    "Claude Opus 4.5": "claude-opus-4-5-20251101",
    "Claude Opus 4": "claude-opus-4-20250514",
    "Claude Sonnet 4": "claude-sonnet-4-20250514",
    "Claude Haiku 4.5": "claude-haiku-4-5-20251001",
}

GOOGLE_MODELS = {
    "Gemini 2.5 Pro": "gemini-2.5-pro",
    "Gemini 2.5 Flash": "gemini-2.5-flash",
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 3 Pro (Preview)": "gemini-3-pro-preview",
    "Gemini 3 Flash (Preview)": "gemini-3-flash-preview",
}

# 全モデルリスト（provider, model_id）
ALL_MODELS = {}
ALL_MODELS.update({k: ("openai", v) for k, v in OPENAI_MODELS.items()})
ALL_MODELS.update({k: ("anthropic", v) for k, v in ANTHROPIC_MODELS.items()})
ALL_MODELS.update({k: ("google", v) for k, v in GOOGLE_MODELS.items()})

# --- プロンプト ---
SYSTEM_PROMPT = """
あなたはアイデアを広げるブレインストーミングのプロです。

【あなたの役割】
前の人のアイデアを踏まえつつ、**別の角度**から新しいアイデアを出してください。

以下のどれかのアプローチを選んで発言してください：
1. **別の視点** - 違う立場（子供、お年寄り、外国人など）から見たらどうなる？
2. **掛け合わせ** - 全然関係ない分野と組み合わせたら？
3. **逆転の発想** - 常識の逆をやったら？
4. **スケール変更** - もっと小さく/大きくしたら？
5. **時間軸を変える** - 10年後/100年前だったら？

【ルール】
- 前の人と同じことを言わない
- 「いいね」「素晴らしい」などの肯定から始めなくていい
- いきなり本題に入ってOK
- 具体例を1つ入れる

【出力形式】
3〜5文で、新しいアイデアを1つだけ提案してください。
"""

FACILITATOR_PROMPT = """
あなたは「難しい話をわかりやすくまとめる」プロです。

以下の対話を、普通の人が読んでスッと理解できるようにまとめてください。

## まとめ

### 一言で言うと
このアイデアを1文で説明してください。小学生でもわかるように。

### 話し合いで出たポイント
{collaborator_list}
それぞれの発言から、良かった点を1つずつ箇条書きで。

### 結局どうすればいい？
明日から始められる具体的なアクションを3つ。
「〜する」という形で、曖昧さなく書いてください。

### こんな人におすすめ
このアイデアが役立ちそうな場面や人を2〜3個。

---
難しい言葉は使わず、友達に説明するつもりで書いてください。
テーマ: {topic}
"""


def get_avatar(model_name: str) -> str:
    """モデル名からアバター絵文字を取得"""
    if any(k in model_name for k in ["GPT", "o3", "o4"]):
        return "🟢"
    elif "Claude" in model_name:
        return "🟣"
    elif "Gemini" in model_name:
        return "🔵"
    return "⚪"


def check_api_keys() -> dict:
    """APIキーの設定状況を確認"""
    return {
        "openai": bool(OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-xxxx")),
        "anthropic": bool(ANTHROPIC_API_KEY and not ANTHROPIC_API_KEY.startswith("sk-ant-xxxx")),
        "google": bool(GOOGLE_API_KEY and not GOOGLE_API_KEY.startswith("AIzaxxxx")),
    }
