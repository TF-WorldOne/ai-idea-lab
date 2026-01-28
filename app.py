"""
AI Idea Lab Pro - 創造的コラボレーションアプリ
複数のAIがアイデアを発展・エンハンスし、最高のアイデアを生み出します
"""
import streamlit as st
import time
from openai import OpenAI
import anthropic
import google.generativeai as genai

from config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY,
    OPENAI_MODELS, ANTHROPIC_MODELS, GOOGLE_MODELS, ALL_MODELS,
    NO_TEMPERATURE_MODELS, SYSTEM_PROMPT, FACILITATOR_PROMPT,
    get_avatar, check_api_keys
)

# --- ページ設定 ---
st.set_page_config(
    page_title="AI Idea Lab Pro",
    page_icon="💡",
    layout="wide"
)

st.title("💡 AI Idea Lab Pro")
st.markdown("複数のAIがアイデアを **発展・エンハンス** し、最高のアイデアを生み出します")

# --- APIキー状況の確認 ---
api_status = check_api_keys()

# --- サイドバー ---
with st.sidebar:
    st.header("🔑 API Keys 状況")
    
    # 設定状況を表示
    for provider, is_set in api_status.items():
        if is_set:
            st.success(f"✅ {provider.upper()}")
        else:
            st.error(f"❌ {provider.upper()}")
    
    if not any(api_status.values()):
        st.warning("⚠️ .envファイルにAPIキーを設定してください")
        st.code("cp .env.example .env\n# .envを編集してAPIキーを追加", language="bash")
    
    st.markdown("---")
    st.header("🤝 コラボレーター選択")
    st.caption("議論に参加するAIを選択（複数可）")
    
    # モデル選択（カテゴリ別）- APIキーがあるものだけ有効化
    st.subheader("OpenAI", divider="green")
    selected_openai = st.multiselect(
        "OpenAIモデル",
        list(OPENAI_MODELS.keys()),
        default=["GPT-4o"] if api_status["openai"] else [],
        disabled=not api_status["openai"],
        label_visibility="collapsed"
    )
    
    st.subheader("Anthropic", divider="violet")
    selected_anthropic = st.multiselect(
        "Anthropicモデル",
        list(ANTHROPIC_MODELS.keys()),
        default=["Claude Sonnet 4"] if api_status["anthropic"] else [],
        disabled=not api_status["anthropic"],
        label_visibility="collapsed"
    )
    
    st.subheader("Google", divider="blue")
    selected_google = st.multiselect(
        "Googleモデル",
        list(GOOGLE_MODELS.keys()),
        default=["Gemini 2.5 Flash"] if api_status["google"] else [],
        disabled=not api_status["google"],
        label_visibility="collapsed"
    )
    
    # 選択されたモデル一覧
    selected_models = selected_openai + selected_anthropic + selected_google
    
    st.markdown("---")
    st.header("🎯 ファシリテーター")
    
    # ファシリテーター候補（選択されていないモデル & APIキーがあるもの）
    available_facilitators = []
    for m, (provider, _) in ALL_MODELS.items():
        if m not in selected_models and api_status.get(provider, False):
            available_facilitators.append(m)
    
    if available_facilitators:
        facilitator = st.selectbox(
            "まとめ役（議論には参加しません）",
            available_facilitators,
            index=0
        )
    else:
        st.warning("⚠️ ファシリテーター用に1つ以上のモデルを残してください")
        facilitator = None
    
    st.markdown("---")
    st.header("⚙️ 設定")
    rounds = st.slider("ラウンド数", 1, 10, 2)
    sleep_time = st.slider("生成間隔（秒）", 0, 5, 1)
    
    # 選択状況の表示
    st.markdown("---")
    if selected_models:
        st.success(f"🤝 参加者: {len(selected_models)}体")
        for m in selected_models:
            st.write(f"  {get_avatar(m)} {m}")
    if facilitator:
        st.info(f"🎯 ファシリテーター: {get_avatar(facilitator)} {facilitator}")


# --- クライアント初期化 ---
@st.cache_resource
def init_clients():
    """APIクライアントを初期化（キャッシュ付き）"""
    clients = {"openai": None, "anthropic": None, "google": None}
    
    if OPENAI_API_KEY:
        try:
            clients["openai"] = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            st.error(f"OpenAI初期化エラー: {e}")
    
    if ANTHROPIC_API_KEY:
        try:
            clients["anthropic"] = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except Exception as e:
            st.error(f"Anthropic初期化エラー: {e}")
    
    if GOOGLE_API_KEY:
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            clients["google"] = True
        except Exception as e:
            st.error(f"Google初期化エラー: {e}")
    
    return clients


# --- AI呼び出し関数 ---
def ask_ai(model_name: str, clients: dict, history_text: str, is_first: bool = False, topic: str = "") -> str:
    """指定されたAIに発言させる"""
    provider, model_id = ALL_MODELS[model_name]
    
    if is_first:
        prompt = f"テーマ: {topic}\n\nこのテーマについて、最初のアイデアを提案してください。ワクワクするような、可能性を感じる提案をお願いします。"
    else:
        prompt = f"これまでの対話:\n{history_text}\n\n前の発言者のアイデアを受けて、さらに発展させてください。「Yes, And」の精神で、アイデアをエンハンスしてください。"
    
    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI APIキーが設定されていません"
            
            params = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ]
            }
            if model_id not in NO_TEMPERATURE_MODELS:
                params["temperature"] = 0.9
            
            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content
        
        elif provider == "anthropic":
            if not clients["anthropic"]:
                return "❌ Anthropic APIキーが設定されていません"
            
            response = clients["anthropic"].messages.create(
                model=model_id,
                max_tokens=1500,
                temperature=0.9,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif provider == "google":
            if not clients["google"]:
                return "❌ Google APIキーが設定されていません"
            
            model = genai.GenerativeModel(model_id)
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text
            
    except Exception as e:
        return f"❌ Error ({model_name}): {e}"


# --- ファシリテーター関数 ---
def facilitate(facilitator_name: str, clients: dict, topic: str, full_log: str, collaborators: list) -> str:
    """対話を統合し、最終アイデアをまとめる"""
    provider, model_id = ALL_MODELS[facilitator_name]
    
    collab_list = "\n".join([f"- **{c}**: (このAIが加えた独自の視点・価値を2-3行で)" for c in collaborators])
    
    facilitator_prompt = FACILITATOR_PROMPT.format(
        topic=topic,
        collaborator_list=collab_list
    )
    full_prompt = f"{facilitator_prompt}\n\n--- 対話ログ ---\n{full_log}"
    
    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI APIキーが設定されていません"
            
            params = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "あなたは創造的な対話のファシリテーターです。"},
                    {"role": "user", "content": full_prompt}
                ]
            }
            if model_id not in NO_TEMPERATURE_MODELS:
                params["temperature"] = 0.5
            
            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content
        
        elif provider == "anthropic":
            if not clients["anthropic"]:
                return "❌ Anthropic APIキーが設定されていません"
            
            response = clients["anthropic"].messages.create(
                model=model_id,
                max_tokens=2500,
                temperature=0.5,
                system="あなたは創造的な対話のファシリテーターです。",
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.content[0].text
        
        elif provider == "google":
            if not clients["google"]:
                return "❌ Google APIキーが設定されていません"
            
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(full_prompt)
            return response.text
            
    except Exception as e:
        return f"❌ ファシリテーターエラー ({facilitator_name}): {e}"


# --- メイン処理 ---
topic = st.text_input(
    "💭 アイデアを発展させたいテーマを入力してください", 
    "地方の過疎化問題を解決する革新的なアプローチ"
)

# バリデーション
can_start = True
error_messages = []

if len(selected_models) < 2:
    error_messages.append("議論には2体以上のAIを選択してください")
    can_start = False

if not facilitator:
    error_messages.append("ファシリテーターを選択してください")
    can_start = False

if not any(api_status.values()):
    error_messages.append(".envファイルにAPIキーを設定してください")
    can_start = False

for msg in error_messages:
    st.warning(f"⚠️ {msg}")

if st.button("🚀 アイデアセッション開始", disabled=not can_start, type="primary"):
    clients = init_clients()
    
    history_log = []
    chat_container = st.container()
    
    with chat_container:
        st.info(f"💭 テーマ: {topic}")
        
        # 参加者表示
        participants_str = " & ".join([f"**{get_avatar(m)} {m}**" for m in selected_models])
        st.markdown(f"🤝 {participants_str}")
        st.markdown(f"🎯 ファシリテーター: **{get_avatar(facilitator)} {facilitator}**")
        st.markdown("---")

        # === 創造的対話フェーズ ===
        for i in range(rounds):
            st.markdown(f"### 💫 ラウンド {i+1}")
            
            for j, model in enumerate(selected_models):
                with st.chat_message("assistant", avatar=get_avatar(model)):
                    if i == 0 and j == 0:
                        st.write(f"**{model}** 💡 最初のアイデア...")
                    else:
                        st.write(f"**{model}** ✨ アイデアを発展...")
                    
                    if i == 0 and j == 0:
                        msg = ask_ai(model, clients, "", is_first=True, topic=topic)
                    else:
                        context_text = "\n\n".join(history_log[-6:])
                        msg = ask_ai(model, clients, context_text)
                    
                    st.write(msg)
                
                history_log.append(f"[{model}]: {msg}")
                time.sleep(sleep_time)
        
        st.success("🎉 対話セッション完了！アイデアを統合します...")
        st.markdown("---")
        
        # === ファシリテーターフェーズ ===
        st.markdown("## 🎯 アイデア統合")
        
        with st.spinner(f"🎯 {facilitator} がアイデアを統合中..."):
            full_log = "\n\n".join(history_log)
            conclusion = facilitate(facilitator, clients, topic, full_log, selected_models)
        
        with st.chat_message("assistant", avatar=get_avatar(facilitator)):
            st.markdown(f"### 🎯 ファシリテーター: {facilitator}")
            st.markdown(conclusion)
        
        st.markdown("---")
        st.balloons()
        
        # ログダウンロード
        participants_list = ", ".join(selected_models)
        full_log_with_conclusion = (
            f"テーマ: {topic}\n"
            f"コラボレーター: {participants_list}\n"
            f"ファシリテーター: {facilitator}\n\n"
            f"{'='*50}\n💬 対話ログ\n{'='*50}\n\n"
            f"{full_log}\n\n"
            f"{'='*50}\n🎯 統合されたアイデア ({facilitator})\n{'='*50}\n\n"
            f"{conclusion}"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "📜 対話ログをダウンロード", 
                full_log, 
                file_name="idea_session_log.txt"
            )
        with col2:
            st.download_button(
                "📋 完全レポートをダウンロード", 
                full_log_with_conclusion, 
                file_name="idea_session_full_report.txt"
            )
