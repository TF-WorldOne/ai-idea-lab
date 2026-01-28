"""
AI Idea Lab Pro - Gemini Canvas Edition
Split view with chat on left and canvas on right
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

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Idea Lab Pro",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Gemini Canvas CSS (Light Mode with Glass effects) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #F0F4F9;
    --bg-card: #FFFFFF;
    --text-primary: #1F1F1F;
    --text-secondary: #5F6368;
    --accent: #1A73E8;
    --accent-light: #E8F0FE;
    --success: #34A853;
    --error: #EA4335;
    --border: rgba(0,0,0,0.08);
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

.main .block-container {
    padding: 1rem 2rem 6rem 2rem;
    max-width: 100% !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-card);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding: 1rem;
}

/* Cards */
.canvas-card {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    min-height: 70vh;
    border: 1px solid var(--border);
}

/* Chat Messages */
.stChatMessage {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
    padding: 1rem !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    border: 1px solid var(--border) !important;
}

/* Input */
.stTextInput input, .stChatInputContainer textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 24px !important;
    padding: 0.75rem 1.25rem !important;
    font-size: 1rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

.stTextInput input:focus, .stChatInputContainer textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-light) !important;
}

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 24px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #1557B0 !important;
    transform: translateY(-1px) !important;
}

/* Status badges */
.stSuccess {
    background: #E6F4EA !important;
    color: var(--success) !important;
    border-radius: 8px !important;
}

.stError {
    background: #FCE8E6 !important;
    color: var(--error) !important;
    border-radius: 8px !important;
}

/* Headers */
h1 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Multiselect */
div[data-baseweb="select"] {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
}

/* Hide default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Download buttons */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
}

.stDownloadButton > button:hover {
    background: var(--accent-light) !important;
}
</style>
""", unsafe_allow_html=True)

# --- API Status ---
api_status = check_api_keys()

# --- Sidebar ---
with st.sidebar:
    st.markdown("## 🔑 API Keys")
    for provider, is_set in api_status.items():
        if is_set:
            st.success(f"✓ {provider.upper()}")
        else:
            st.error(f"✗ {provider.upper()}")

    st.markdown("---")
    st.markdown("## 🤝 コラボレーター")

    selected_openai = st.multiselect(
        "OpenAI",
        list(OPENAI_MODELS.keys()),
        default=["GPT-4o"] if api_status["openai"] else [],
        disabled=not api_status["openai"]
    )

    selected_anthropic = st.multiselect(
        "Anthropic",
        list(ANTHROPIC_MODELS.keys()),
        default=["Claude Sonnet 4"] if api_status["anthropic"] else [],
        disabled=not api_status["anthropic"]
    )

    selected_google = st.multiselect(
        "Google",
        list(GOOGLE_MODELS.keys()),
        default=["Gemini 2.5 Flash"] if api_status["google"] else [],
        disabled=not api_status["google"]
    )

    selected_models = selected_openai + selected_anthropic + selected_google

    st.markdown("---")
    st.markdown("## 🎯 ファシリテーター")

    available_facilitators = []
    for m, (provider, _) in ALL_MODELS.items():
        if m not in selected_models and api_status.get(provider, False):
            available_facilitators.append(m)

    if available_facilitators:
        facilitator = st.selectbox("まとめ役", available_facilitators)
    else:
        st.warning("⚠️ モデルを残してください")
        facilitator = None

    st.markdown("---")
    st.markdown("## ⚙️ 設定")
    rounds = st.slider("ラウンド数", 1, 10, 2)


# --- Initialize Clients ---
@st.cache_resource
def init_clients():
    clients = {"openai": None, "anthropic": None, "google": None}
    if OPENAI_API_KEY:
        try:
            clients["openai"] = OpenAI(api_key=OPENAI_API_KEY)
        except Exception:
            pass
    if ANTHROPIC_API_KEY:
        try:
            clients["anthropic"] = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        except Exception:
            pass
    if GOOGLE_API_KEY:
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            clients["google"] = True
        except Exception:
            pass
    return clients


# --- AI Call Function ---
def ask_ai(model_name: str, clients: dict, history_text: str, is_first: bool = False, topic: str = "") -> str:
    provider, model_id = ALL_MODELS[model_name]

    if is_first:
        prompt = f"テーマ: {topic}\n\nこのテーマについて、最初のアイデアを提案してください。"
    else:
        prompt = f"これまでの対話:\n{history_text}\n\n前の発言者のアイデアを受けて、さらに発展させてください。"

    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI APIキーが未設定"
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
                return "❌ Anthropic APIキーが未設定"
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
                return "❌ Google APIキーが未設定"
            model = genai.GenerativeModel(model_id)
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text

    except Exception as e:
        return f"❌ Error ({model_name}): {e}"


# --- Facilitator Function ---
def facilitate(facilitator_name: str, clients: dict, topic: str, full_log: str, collaborators: list) -> str:
    provider, model_id = ALL_MODELS[facilitator_name]

    collab_list = "\n".join([f"- **{c}**" for c in collaborators])
    facilitator_prompt = FACILITATOR_PROMPT.format(topic=topic, collaborator_list=collab_list)
    full_prompt = f"{facilitator_prompt}\n\n--- 対話ログ ---\n{full_log}"

    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI APIキーが未設定"
            params = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "あなたは対話のファシリテーターです。"},
                    {"role": "user", "content": full_prompt}
                ]
            }
            if model_id not in NO_TEMPERATURE_MODELS:
                params["temperature"] = 0.5
            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content

        elif provider == "anthropic":
            if not clients["anthropic"]:
                return "❌ Anthropic APIキーが未設定"
            response = clients["anthropic"].messages.create(
                model=model_id,
                max_tokens=2500,
                temperature=0.5,
                system="あなたは対話のファシリテーターです。",
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.content[0].text

        elif provider == "google":
            if not clients["google"]:
                return "❌ Google APIキーが未設定"
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(full_prompt)
            return response.text

    except Exception as e:
        return f"❌ ファシリテーターエラー ({facilitator_name}): {e}"


# --- Session State ---
if "conclusion" not in st.session_state:
    st.session_state.conclusion = None
if "facilitator_name" not in st.session_state:
    st.session_state.facilitator_name = None
if "full_report" not in st.session_state:
    st.session_state.full_report = None


# --- Main Layout ---
st.title("💡 AI Idea Lab Pro")

col_input, col_canvas = st.columns([1, 1.5], gap="large")

with col_input:
    st.markdown("### 💭 テーマを入力")
    topic = st.text_area(
        "テーマ",
        "地方の過疎化問題を解決する革新的なアプローチ",
        height=100,
        label_visibility="collapsed"
    )

    # Validation
    can_start = True
    if len(selected_models) < 2:
        st.warning("⚠️ 2体以上のAIを選択してください")
        can_start = False
    if not facilitator:
        st.warning("⚠️ ファシリテーターを選択してください")
        can_start = False

    start_button = st.button("🚀 セッション開始", disabled=not can_start, type="primary", use_container_width=True)

# --- Run Session ---
if start_button:
    clients = init_clients()
    history_log = []

    with col_input:
        st.markdown("---")
        st.markdown(f"**テーマ:** {topic}")
        st.markdown(f"**参加者:** {', '.join(selected_models)}")
        st.markdown(f"**ファシリテーター:** {facilitator}")
        st.markdown("---")

        # Collaboration Phase
        for i in range(rounds):
            st.markdown(f"#### 💫 ラウンド {i+1}")

            for j, model in enumerate(selected_models):
                with st.chat_message("assistant", avatar=get_avatar(model)):
                    st.markdown(f"**{model}**")

                    if i == 0 and j == 0:
                        msg = ask_ai(model, clients, "", is_first=True, topic=topic)
                    else:
                        context_text = "\n\n".join(history_log[-6:])
                        msg = ask_ai(model, clients, context_text)

                    st.write(msg)

                history_log.append(f"[{model}]: {msg}")
                time.sleep(0.5)

        st.success("🎉 対話完了！まとめ中...")

    # Update Canvas with results
    full_log = "\n\n".join(history_log)

    with st.spinner(f"🎯 {facilitator} がまとめ中..."):
        conclusion = facilitate(facilitator, clients, topic, full_log, selected_models)

    # Save to session state
    st.session_state.conclusion = conclusion
    st.session_state.facilitator_name = facilitator
    st.session_state.full_report = f"テーマ: {topic}\n\n{full_log}\n\n--- まとめ ---\n{conclusion}"

    st.balloons()

# --- Canvas Display ---
with col_canvas:
    if st.session_state.conclusion:
        st.markdown("### 🎯 アイデア統合レポート")
        with st.chat_message("assistant", avatar=get_avatar(st.session_state.facilitator_name)):
            st.markdown(f"**{st.session_state.facilitator_name}**")
            st.markdown(st.session_state.conclusion)

        st.download_button(
            "📥 レポートをダウンロード",
            st.session_state.full_report,
            "idea_lab_report.txt",
            use_container_width=True
        )

        if st.button("🔄 リセット", use_container_width=True):
            st.session_state.conclusion = None
            st.session_state.facilitator_name = None
            st.session_state.full_report = None
            st.rerun()
    else:
        st.markdown("""
        <div class="canvas-card">
            <h2>📋 Canvas</h2>
            <p style="color: #5F6368;">セッションを開始すると、ここにアイデアが表示されます</p>
        </div>
        """, unsafe_allow_html=True)
