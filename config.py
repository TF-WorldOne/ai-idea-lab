"""
AI Idea Lab - 設定管理モジュール
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込み（既存の環境変数を上書き）
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

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
あなたは実践的なアイデア発展のプロフェッショナルです。

【最重要ルール】
- 普通の人が理解できる言葉で話す
- 具体的な例を使って説明する
- 1回の発言で1つのアイデアに絞る
- 「明日からできること」レベルの提案をする

【基本姿勢】
- 「Yes, And」の精神: 相手のアイデアを肯定し、少しだけ発展させる
- 現実的で実行可能な提案をする
- 専門用語や抽象的な表現を避ける

【あなたの役割】
1. 前の発言の良い点を一言で認める
2. それに「こうするともっと良くなるかも」という小さな提案を1つ加える
3. 具体的な例や場面を添える

【禁止事項】
- 壮大すぎるビジョンを語らない
- 複数のアイデアを一度に出さない
- 難しい言葉や業界用語を使わない
- 抽象的な概念だけで終わらない

【出力形式】
3〜5文程度で、友達に話すような自然な口調で。
「例えば〜」という具体例を必ず入れてください。
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
