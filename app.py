"""
AI Idea Lab Pro - Modern AI Dark Theme Edition
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

# --- Modern AI Dark Theme CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap');

/* ===== CSS Variables (Modern AI Dark - Deep Sky Blue) ===== */
:root {
    --bg-main: #0E1117;
    --bg-sidebar: #161B22;
    --bg-card: #1F2937;
    --bg-input: #0D1117;
    --text-primary: #E6E6E6;
    --text-secondary: #A1A1AA;
    --accent-blue: #1E90FF;
    --accent-blue-hover: #1873CC;
    --accent-purple: #8B5CF6;
    --accent-blue-dim: rgba(30, 144, 255, 0.2);
    --accent-purple-dim: rgba(139, 92, 246, 0.2);
    --success: #10B981;
    --error: #EF4444;
    --border: #374151;
    --border-dim: #30363D;
}

/* ===== Base Styles ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], [class*="css"] {
    background-color: var(--bg-main) !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 1.5rem 2rem 6rem 2rem;
    max-width: 100% !important;
}

/* ===== Typography & Headers ===== */
h1 {
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    background: linear-gradient(135deg, #1E90FF 0%, var(--accent-purple) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem !important;
}

h2 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em !important;
}

h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
}

p, span, label, div {
    color: var(--text-primary) !important;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem;
}

section[data-testid="stSidebar"] h2 {
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em !important;
    color: var(--text-secondary) !important;
    margin-bottom: 0.75rem !important;
}

/* ===== Cards & Containers ===== */
.canvas-card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid var(--border);
    min-height: 70vh;
}

.canvas-card h2 {
    color: var(--text-primary) !important;
    margin-bottom: 1rem;
}

.canvas-card p {
    color: var(--text-secondary) !important;
}

/* ===== Chat Messages ===== */
[data-testid="stChatMessage"] {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    margin-bottom: 1rem !important;
    padding: 1.25rem !important;
    border: 1px solid var(--border) !important;
}

[data-testid="stChatMessage"] p {
    color: var(--text-primary) !important;
}

/* ===== Input Fields ===== */
.stTextInput input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px var(--accent-blue-dim) !important;
}

/* Text Area (Topic Input) */
.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 2px solid var(--border-dim) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    color: var(--text-primary) !important;
    transition: all 0.2s ease !important;
    min-height: 100px !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px var(--accent-blue-dim) !important;
}

.stTextArea textarea::placeholder {
    color: var(--text-secondary) !important;
}

/* ===== Buttons ===== */
.stButton > button {
    background: var(--accent-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(30, 144, 255, 0.3) !important;
}

.stButton > button:hover {
    background: var(--accent-blue-hover) !important;
    box-shadow: 0 4px 16px rgba(30, 144, 255, 0.4) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button:disabled {
    background: var(--border) !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* Download Button */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent-blue) !important;
    border: 1px solid var(--accent-blue) !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: var(--accent-blue-dim) !important;
    box-shadow: none !important;
}

/* ===== Status Badges (Pill Style) ===== */
.stSuccess {
    background: rgba(16, 185, 129, 0.15) !important;
    color: var(--success) !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(16, 185, 129, 0.3) !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    color: var(--error) !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
}

.stWarning {
    background: rgba(245, 158, 11, 0.15) !important;
    color: #F59E0B !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
}

/* ===== Multiselect & Select ===== */
div[data-baseweb="select"] {
    background: var(--bg-input) !important;
}

div[data-baseweb="select"] > div {
    background: var(--bg-input) !important;
    border-color: var(--border-dim) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px var(--accent-blue-dim) !important;
}

/* Selected tags in multiselect */
span[data-baseweb="tag"] {
    background: var(--accent-blue-dim) !important;
    color: var(--accent-blue) !important;
    border-radius: 6px !important;
    border: none !important;
}

/* Dropdown menu */
ul[data-baseweb="menu"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

li[data-baseweb="menu-item"] {
    color: var(--text-primary) !important;
}

li[data-baseweb="menu-item"]:hover {
    background: var(--accent-blue-dim) !important;
}

/* ===== Slider ===== */
.stSlider > div > div > div {
    background: var(--border) !important;
}

.stSlider > div > div > div > div {
    background: var(--accent-blue) !important;
}

.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent-blue) !important;
    border-color: var(--accent-blue) !important;
}

/* ===== Spinner ===== */
.stSpinner > div {
    border-top-color: var(--accent-blue) !important;
}

/* ===== Markdown Links ===== */
a {
    color: var(--accent-blue) !important;
}

a:hover {
    color: var(--accent-purple) !important;
}

/* ===== Divider ===== */
hr {
    border-color: var(--border) !important;
    opacity: 0.5 !important;
}

/* ===== Hide Default Elements ===== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ===== Scrollbar ===== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-main);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}

/* ===== Custom Badge Component ===== */
.api-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.375rem 0.875rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.25rem 0;
}

.api-badge.connected {
    background: rgba(16, 185, 129, 0.15);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.api-badge.disconnected {
    background: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ===== Round indicator ===== */
.round-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1E90FF 0%, var(--accent-purple) 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-right: 0.5rem;
}

/* ===== Model name badge ===== */
.model-badge {
    display: inline-block;
    background: var(--accent-purple-dim);
    color: var(--accent-purple);
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
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
            st.markdown(f'<div class="api-badge connected">✓ {provider.upper()}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="api-badge disconnected">✗ {provider.upper()}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🤝 Collaborators")

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
    st.markdown("## 🎯 Facilitator")

    available_facilitators = []
    for m, (provider, _) in ALL_MODELS.items():
        if m not in selected_models and api_status.get(provider, False):
            available_facilitators.append(m)

    if available_facilitators:
        facilitator = st.selectbox("Summary Host", available_facilitators)
    else:
        st.warning("⚠️ Please keep at least one model available")
        facilitator = None

    st.markdown("---")
    st.markdown("## ⚙️ Settings")
    rounds = st.slider("Number of Rounds", 1, 10, 2)


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
        prompt = f"Topic: {topic}\n\nPlease propose your initial idea on this topic."
    else:
        prompt = f"Discussion so far:\n{history_text}\n\nBuild upon the previous ideas and add your unique perspective."

    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI API key not configured"
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
                return "❌ Anthropic API key not configured"
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
                return "❌ Google API key not configured"
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
    full_prompt = f"{facilitator_prompt}\n\n--- Discussion Log ---\n{full_log}"

    try:
        if provider == "openai":
            if not clients["openai"]:
                return "❌ OpenAI API key not configured"
            params = {
                "model": model_id,
                "messages": [
                    {"role": "system", "content": "You are a discussion facilitator."},
                    {"role": "user", "content": full_prompt}
                ]
            }
            if model_id not in NO_TEMPERATURE_MODELS:
                params["temperature"] = 0.5
            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content

        elif provider == "anthropic":
            if not clients["anthropic"]:
                return "❌ Anthropic API key not configured"
            response = clients["anthropic"].messages.create(
                model=model_id,
                max_tokens=2500,
                temperature=0.5,
                system="You are a discussion facilitator.",
                messages=[{"role": "user", "content": full_prompt}]
            )
            return response.content[0].text

        elif provider == "google":
            if not clients["google"]:
                return "❌ Google API key not configured"
            model = genai.GenerativeModel(model_id)
            response = model.generate_content(full_prompt)
            return response.text

    except Exception as e:
        return f"❌ Facilitator Error ({facilitator_name}): {e}"


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
    st.markdown("### 💭 Enter Your Topic")
    topic = st.text_area(
        "Topic",
        "Innovative approaches to solve rural depopulation",
        height=100,
        label_visibility="collapsed"
    )

    # Validation
    can_start = True
    if len(selected_models) < 2:
        st.warning("⚠️ Please select at least 2 AI collaborators")
        can_start = False
    if not facilitator:
        st.warning("⚠️ Please select a facilitator")
        can_start = False

    start_button = st.button("🚀 Start Session", disabled=not can_start, type="primary", use_container_width=True)

# --- Run Session ---
if start_button:
    clients = init_clients()
    history_log = []

    with col_input:
        st.markdown("---")
        st.markdown(f"**Topic:** {topic}")
        st.markdown(f"**Participants:** {', '.join(selected_models)}")
        st.markdown(f"**Facilitator:** {facilitator}")
        st.markdown("---")

        # Collaboration Phase
        for i in range(rounds):
            st.markdown(f'<span class="round-badge">Round {i+1}</span>', unsafe_allow_html=True)

            for j, model in enumerate(selected_models):
                with st.chat_message("assistant", avatar=get_avatar(model)):
                    st.markdown(f'<span class="model-badge">{model}</span>', unsafe_allow_html=True)

                    if i == 0 and j == 0:
                        msg = ask_ai(model, clients, "", is_first=True, topic=topic)
                    else:
                        context_text = "\n\n".join(history_log[-6:])
                        msg = ask_ai(model, clients, context_text)

                    st.write(msg)

                history_log.append(f"[{model}]: {msg}")
                time.sleep(0.5)

        st.success("🎉 Discussion complete! Generating summary...")

    # Update Canvas with results
    full_log = "\n\n".join(history_log)

    with st.spinner(f"🎯 {facilitator} is creating the summary..."):
        conclusion = facilitate(facilitator, clients, topic, full_log, selected_models)

    # Save to session state
    st.session_state.conclusion = conclusion
    st.session_state.facilitator_name = facilitator
    st.session_state.full_report = f"Topic: {topic}\n\n{full_log}\n\n--- Summary ---\n{conclusion}"

    st.balloons()

# --- Canvas Display ---
with col_canvas:
    if st.session_state.conclusion:
        st.markdown("### 🎯 Idea Synthesis Report")
        with st.chat_message("assistant", avatar=get_avatar(st.session_state.facilitator_name)):
            st.markdown(f'<span class="model-badge">{st.session_state.facilitator_name}</span>', unsafe_allow_html=True)
            st.markdown(st.session_state.conclusion)

        st.download_button(
            "📥 Download Report",
            st.session_state.full_report,
            "idea_lab_report.txt",
            use_container_width=True
        )

        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.conclusion = None
            st.session_state.facilitator_name = None
            st.session_state.full_report = None
            st.rerun()
    else:
        st.markdown("""
        <div class="canvas-card">
            <h2>📋 Canvas</h2>
            <p>Start a session to see the Idea Synthesis Report here</p>
        </div>
        """, unsafe_allow_html=True)
