"""
X-Think AI Idea Lab - Premium Edition
Three-column layout with no sidebar
"""
import streamlit as st
import time
import base64
import re
import requests
import io
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from openai import OpenAI
import anthropic
import google.generativeai as genai

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None

from config import (
    OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY,
    OPENAI_MODELS, ANTHROPIC_MODELS, GOOGLE_MODELS, ALL_MODELS,
    NO_TEMPERATURE_MODELS, get_system_prompt, get_facilitator_prompt,
    get_avatar, check_api_keys,
    # Personality system
    AI_PERSONALITIES, PERSONALITY_MODES,
    get_personality_info, get_personality_avatar, get_all_personality_ids,
    # URL reading
    URL_READING_CONFIG, URL_PATTERN, URL_ANALYSIS_PROMPT_ADDITION,
    # Dynamic expertise
    EXPERTISE_EXTRACTION_PROMPT, DYNAMIC_EXPERTISE_PROMPT_TEMPLATE,
    # File upload
    FILE_UPLOAD_CONFIG, VISION_ANALYSIS_PROMPT,
    # NotebookLM settings
    NOTEBOOKLM_ENABLED, NOTEBOOKLM_REGION, GCP_PROJECT_NUMBER,
    DEFAULT_FACILITATOR,
    # Synthesis report formats
    SYNTHESIS_FORMATS, get_facilitator_prompt_by_format
)



# NotebookLM integration
try:
    from notebooklm_integration import export_discussion_to_notebooklm
    NOTEBOOKLM_AVAILABLE = True
except ImportError:
    NOTEBOOKLM_AVAILABLE = False
st.set_page_config(
    page_title="X-Think AI Idea Lab",
    page_icon="assets/siteicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Logo Helper Function ---
def get_logo_base64():
    """Load logo as base64 for embedding"""
    logo_path = Path(__file__).parent / "assets" / "xexon_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None


def show_star_celebration():
    """Display gold star celebration animation"""
    import random
    stars_html = '<div class="star-celebration">'
    for i in range(30):
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        duration = random.uniform(2, 4)
        size = random.randint(16, 32)
        stars_html += f'<span class="star" style="left: {left}%; animation-delay: {delay}s; animation-duration: {duration}s; font-size: {size}px;">✦</span>'
    stars_html += '</div>'
    st.markdown(stars_html, unsafe_allow_html=True)

# --- X-Think Premium Gold & Black Theme CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+JP:wght@400;500;700&display=swap');

/* ===== CSS Variables (X-Think Premium - Gold & Black) ===== */
:root {
    --bg-main: #050505;
    --bg-card: #1F1F1F;
    --bg-input: #0A0A0A;
    --text-primary: #F0F0F0;
    --text-secondary: #A0A0A0;
    --accent-gold: #D4AF37;
    --accent-gold-hover: #B8960F;
    --accent-gold-dim: rgba(212, 175, 55, 0.2);
    --accent-gold-glow: rgba(212, 175, 55, 0.4);
    --success: #D4AF37;
    --error: #EF4444;
    --border: #2A2A2A;
    --border-dim: #1A1A1A;
}

/* ===== Base Styles ===== */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], [class*="css"] {
    background-color: var(--bg-main) !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
}

/* ===== Sidebar Styling ===== */
/* Style sidebar with dark theme */
section[data-testid="stSidebar"] {
    background-color: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

/* FORCE sidebar collapse/expand button to be visible */
/* Target all possible selectors for Streamlit sidebar toggle */
button[data-testid="stSidebarCollapsedControl"],
button[data-testid="baseButton-headerNoPadding"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="collapsedControl"],
div[data-testid="stSidebarCollapsedControl"],
.stSidebarCollapsedControl,
/* Streamlit 1.30+ uses different class names */
button[kind="headerNoPadding"],
[data-testid="stSidebarNavCollapseButton"],
section[data-testid="stSidebarCollapsedControl"] button {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    background-color: var(--accent-gold) !important;
    color: var(--bg-main) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    margin: 8px !important;
    position: fixed !important;
    top: 60px !important;
    left: 8px !important;
    z-index: 999999 !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(212, 175, 55, 0.5) !important;
}

/* Style the arrow/icon inside the button */
button[data-testid="stSidebarCollapsedControl"] svg,
button[data-testid="baseButton-headerNoPadding"] svg {
    fill: var(--bg-main) !important;
    color: var(--bg-main) !important;
}

/* Hide Streamlit header completely */
header[data-testid="stHeader"],
.stHeader,
[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}

/* Hide top decoration bar */
[data-testid="stDecoration"],
.stDecoration {
    display: none !important;
    height: 0 !important;
}

/* Hide toolbar */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Remove ALL padding from main containers */
.main .block-container,
[data-testid="stAppViewBlockContainer"],
.stMainBlockContainer,
[data-testid="stMainBlockContainer"] {
    padding-top: 0 !important;
    padding-bottom: 1rem !important;
    margin-top: 0 !important;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Ensure the app view starts at the very top */
.stApp,
[data-testid="stApp"] {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

.stAppViewMain,
[data-testid="stAppViewMain"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Force the main container to have no top spacing */
.stMain,
[data-testid="stMain"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

/* Remove any iframe padding */
iframe {
    margin: 0 !important;
    padding: 0 !important;
}

/* ===== Typography & Headers ===== */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
}

h1 {
    background: linear-gradient(135deg, #D4AF37 0%, #F5E6A3 50%, #D4AF37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem !important;
    text-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
}

h2 {
    color: var(--accent-gold) !important;
}

h3 {
    color: var(--text-primary) !important;
    font-size: 1.05em !important;
}

/* Report heading styles - unified 0.9rem with bold */
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4,
[data-testid="stChatMessage"] h5,
[data-testid="stChatMessage"] h6 {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin-top: 1rem !important;
    margin-bottom: 0.5rem !important;
}

/* Hide header anchor links */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    display: none !important;
}

p, label {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
}

/* Separate rule for div without font-family to not break icon fonts */
div {
    color: var(--text-primary) !important;
}

/* ===== Logo Container ===== */
.logo-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.75rem;
    padding: 0.75rem 0 0 0;
}

.logo-container img {
    height: 45px;
    width: auto;
}

/* ===== Column Cards ===== */
.column-card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid var(--border);
    min-height: 400px;
    position: relative;
}

.column-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}

.column-card h3 {
    color: var(--accent-gold) !important;
    margin-bottom: 1rem;
    font-size: 1.1rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em !important;
}

/* ===== Section Headers ===== */
.section-header {
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em !important;
    color: var(--accent-gold) !important;
    margin-bottom: 0.5rem !important;
    margin-top: 1rem !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}

/* ===== Cards & Containers ===== */
.canvas-card {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 2rem;
    border: 1px solid var(--border);
    min-height: 70vh;
    position: relative;
}

.canvas-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
}

.canvas-card h2 {
    color: var(--accent-gold) !important;
    margin-bottom: 1rem;
}

.canvas-card p {
    color: var(--text-secondary) !important;
}

.report-title {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    color: var(--accent-gold) !important;
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
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
}

[data-testid="stChatMessage"] ol,
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] li *,
[data-testid="stChatMessage"] ol *,
[data-testid="stChatMessage"] ul * {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
}

[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] em,
[data-testid="stChatMessage"] span {
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
}

/* ===== Input Fields ===== */
.stTextInput input {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 3px var(--accent-gold-dim) !important;
}

/* Text Area (Topic Input) */
.stTextArea {
    border: none !important;
    outline: none !important;
}

.stTextArea > div {
    border: none !important;
    outline: none !important;
    background: transparent !important;
}

.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
    min-height: 100px !important;
}

.stTextArea textarea:focus {
    border: 3px solid var(--accent-gold) !important;
    border-radius: 12px !important;
    outline: none !important;
    box-shadow: none !important;
}

.stTextArea textarea::placeholder {
    color: var(--text-secondary) !important;
}

/* ===== Buttons ===== */
.stButton > button,
[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #D4AF37 0%, #B8960F 100%) !important;
    color: #050505 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 12px rgba(212, 175, 55, 0.3) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stButton > button:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    background: linear-gradient(135deg, #F5E6A3 0%, #D4AF37 100%) !important;
    box-shadow: 0 4px 20px rgba(212, 175, 55, 0.5) !important;
    transform: translateY(-2px) !important;
    color: #050505 !important;
}

.stButton > button:active,
[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
}

.stButton > button:disabled,
[data-testid="stFormSubmitButton"] > button:disabled {
    background: var(--border) !important;
    color: var(--text-secondary) !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* Download Button */
.stDownloadButton > button {
    background: transparent !important;
    color: var(--accent-gold) !important;
    border: 1px solid var(--accent-gold) !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: var(--accent-gold-dim) !important;
    box-shadow: 0 0 15px var(--accent-gold-dim) !important;
}

/* ===== Status Badges (Pill Style) ===== */
.stSuccess {
    background: rgba(212, 175, 55, 0.15) !important;
    color: var(--accent-gold) !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(212, 175, 55, 0.3) !important;
}

.stError {
    background: rgba(239, 68, 68, 0.15) !important;
    color: var(--error) !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(239, 68, 68, 0.3) !important;
}

.stWarning {
    background: rgba(212, 175, 55, 0.15) !important;
    color: var(--accent-gold) !important;
    border-radius: 9999px !important;
    padding: 0.25rem 0.75rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    border: 1px solid rgba(212, 175, 55, 0.3) !important;
}

/* ===== Multiselect & Select ===== */
div[data-baseweb="select"] {
    background: var(--bg-input) !important;
}

div[data-baseweb="select"] > div {
    background: var(--bg-input) !important;
    border-color: var(--border-dim) !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}

div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 3px var(--accent-gold-dim) !important;
}

/* Selected tags in multiselect */
span[data-baseweb="tag"] {
    background: var(--accent-gold-dim) !important;
    color: var(--accent-gold) !important;
    border-radius: 6px !important;
    border: none !important;
    font-size: 0.9rem !important;
}

/* Dropdown menu */
ul[data-baseweb="menu"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 4px !important;
}

li[data-baseweb="menu-item"] {
    color: var(--text-primary) !important;
    font-size: 0.9rem !important;
    cursor: pointer !important;
    border-radius: 4px !important;
}

li[data-baseweb="menu-item"]:hover,
li[data-baseweb="menu-item"]:focus {
    background-color: var(--accent-gold-dim) !important;
}

/* File uploader text */
[data-testid="stFileUploader"] {
    font-size: 0.9rem !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] button {
    font-size: 0.9rem !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #e0e0e0 !important;
}

/* ===== Radio Buttons & Checkboxes ===== */
/* Radio buttons and checkboxes use default Streamlit styling */

/* Checkbox text color only */
[data-testid="stCheckbox"] p {
    color: var(--text-primary) !important;
}

/* Checkbox */
[data-testid="stCheckbox"] label span[data-testid="stMarkdownContainer"] p {
    color: var(--text-primary) !important;
}

[data-testid="stCheckbox"] input:checked + div {
    background-color: var(--accent-gold) !important;
    border-color: var(--accent-gold) !important;
}

[data-testid="stCheckbox"] input:checked + div svg {
    fill: #000000 !important;
}

/* File uploader dropzone - KILL THE GREEN */
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"] {
    background-color: var(--bg-input) !important;
    border: 1px dashed var(--border) !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:hover {
    border-color: var(--accent-gold) !important;
    background-color: var(--accent-gold-dim) !important;
}

[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:focus,
[data-testid="stFileUploader"] section[data-testid="stFileUploaderDropzone"]:active {
    border-color: var(--accent-gold) !important;
    outline: none !important;
    box-shadow: 0 0 0 2px var(--accent-gold-dim) !important;
}

/* Browse Files Button Style Override */
[data-testid="stFileUploader"] button[kind="secondary"] {
    background-color: transparent !important;
    color: var(--accent-gold) !important;
    border: 1px solid var(--accent-gold) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

[data-testid="stFileUploader"] button[kind="secondary"]:hover {
    background-color: var(--accent-gold-dim) !important;
    border-color: var(--accent-gold) !important;
    color: var(--accent-gold) !important;
}

[data-testid="stFileUploader"] button[kind="secondary"]:active {
    background-color: var(--accent-gold) !important;
    color: #000000 !important;
}

/* Text Area (Topic Input) - KILL THE GREEN & WHITE CORNERS */
.stTextArea {
    border: none !important;
    outline: none !important;
    background-color: transparent !important;
}

.stTextArea > div {
    border: none !important;
    outline: none !important;
    background-color: transparent !important;
}

/* Target the actual textarea element */
.stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 0.9rem !important;
    color: var(--text-primary) !important;
    transition: all 0.3s ease !important;
    min-height: 100px !important;
}

.stTextArea textarea:focus {
    border-color: var(--accent-gold) !important;
    box-shadow: 0 0 0 1px var(--accent-gold) !important;
    outline: none !important;
    border-radius: 8px !important; /* Ensure match on focus */
}

/* Override Streamlit's default focus container styling */
.stTextArea div[data-baseweb="textarea"], 
.stTextArea div[data-baseweb="base-input"] {
    border-color: transparent !important;
    background-color: transparent !important;
    border-radius: 8px !important;
}

.stTextArea div[data-baseweb="textarea"]:focus-within {
    border-color: transparent !important;
    box-shadow: none !important;
}

.stSlider > div > div > div {
    background: var(--border) !important;
}

.stSlider > div > div > div > div {
    background: var(--accent-gold) !important;
}

.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent-gold) !important;
    border-color: var(--accent-gold) !important;
}

/* ===== Expander ===== */
.streamlit-expanderHeader,
.streamlit-expanderHeader span,
.streamlit-expanderHeader p {
    background: var(--bg-input) !important;
    border-radius: 8px !important;
    border: 1px solid var(--border-dim) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.05em !important;
    letter-spacing: 0.05em !important;
}

.streamlit-expanderHeader span,
.streamlit-expanderHeader p {
    background: transparent !important;
    border: none !important;
}

/* Hide the arrow icon text (shows as "arrow_" when font fails to load) */
.streamlit-expanderHeader svg {
    display: block !important;
}

[data-testid="stExpander"] summary span[data-testid="stMarkdownContainer"] {
    overflow: hidden !important;
}

.streamlit-expanderHeader:hover {
    border-color: var(--accent-gold) !important;
}

/* Hide empty expander header (when using separate h3) */
.streamlit-expanderHeader:empty,
.streamlit-expanderHeader:has(p:empty) {
    display: none !important;
}

/* Also hide if the text content is empty */
[data-testid="stExpander"] summary {
    display: none !important;
}

details[open] > summary {
    border-bottom: 1px solid var(--border) !important;
    margin-bottom: 1rem !important;
}

/* ===== Spinner ===== */
.stSpinner > div {
    border-top-color: var(--accent-gold) !important;
}

/* ===== Markdown Links ===== */
a {
    color: var(--accent-gold) !important;
}

a:hover {
    color: #F5E6A3 !important;
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
    background: var(--accent-gold);
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
    background: rgba(212, 175, 55, 0.15);
    color: #D4AF37;
    border: 1px solid rgba(212, 175, 55, 0.3);
}

.api-badge.disconnected {
    background: rgba(239, 68, 68, 0.15);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

/* ===== Round indicator ===== */
.round-badge {
    display: inline-block;
    background: linear-gradient(135deg, #D4AF37 0%, #B8960F 100%);
    color: #050505;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 700;
    margin-right: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ===== Model name badge ===== */
.model-badge {
    display: inline-block;
    background: var(--accent-gold-dim);
    color: var(--accent-gold);
    padding: 0.25rem 0.75rem;
    border-radius: 6px;
    font-size: 0.875rem;
    font-weight: 600;
    border: 1px solid rgba(212, 175, 55, 0.3);
}

/* ===== Premium Border Glow Effect ===== */
.premium-border {
    position: relative;
    border: 1px solid var(--border);
    border-radius: 12px;
}

.premium-border::after {
    content: '';
    position: absolute;
    top: -1px;
    left: -1px;
    right: -1px;
    bottom: -1px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), transparent, rgba(212, 175, 55, 0.1));
    pointer-events: none;
}

/* ===== Gold Star Celebration Animation ===== */
@keyframes starfall {
    0% {
        transform: translateY(-100vh) rotate(0deg);
        opacity: 1;
    }
    100% {
        transform: translateY(100vh) rotate(720deg);
        opacity: 0;
    }
}

@keyframes sparkle {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
}

.star-celebration {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
}

.star {
    position: absolute;
    top: -50px;
    color: #D4AF37;
    font-size: 24px;
    animation: starfall 3s ease-in forwards, sparkle 0.5s ease-in-out infinite;
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.8), 0 0 20px rgba(212, 175, 55, 0.5);
}

/* ===== Report Title (Light Font) ===== */
.report-title {
    font-weight: 300 !important;
    letter-spacing: 0.05em !important;
    color: var(--accent-gold) !important;
}

/* ===== Generating Spinner ===== */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.generating-spinner {
    width: 40px;
    height: 40px;
    margin: 20px auto;
    border: 3px solid var(--border);
    border-top: 3px solid var(--accent-gold);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

/* ===== Personality Badge ===== */
.personality-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-left: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# --- API Status ---
api_status = check_api_keys()

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


# --- URL Detection and Content Fetching ---
def detect_url(text: str) -> str | None:
    """Detect first URL in text"""
    match = re.search(URL_PATTERN, text)
    return match.group(0) if match else None


def fetch_url_content(url: str) -> dict:
    """
    Fetch and extract content from URL
    Returns: {"success": bool, "title": str, "content": str, "error": str}
    """
    if not URL_READING_CONFIG.get("enabled", True):
        return {"success": False, "title": "", "content": "", "error": "URL reading disabled"}
    
    try:
        headers = {"User-Agent": URL_READING_CONFIG.get("user_agent", "")}
        response = requests.get(
            url, 
            headers=headers, 
            timeout=URL_READING_CONFIG.get("timeout", 10)
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script, style, nav, footer elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string.strip() if soup.title.string else ""
        elif soup.find('h1'):
            title = soup.find('h1').get_text(strip=True)
        
        # Extract main content (try common article selectors)
        content = ""
        article_selectors = ['article', 'main', '.article-body', '.post-content', '#content', '.entry-content']
        
        for selector in article_selectors:
            article = soup.select_one(selector)
            if article:
                content = article.get_text(separator='\n', strip=True)
                break
        
        # Fallback: get body text
        if not content:
            body = soup.find('body')
            if body:
                content = body.get_text(separator='\n', strip=True)
        
        # Truncate if too long
        max_length = URL_READING_CONFIG.get("max_content_length", 8000)
        if len(content) > max_length:
            content = content[:max_length] + "\n\n[... Article content truncated ...]"
        
        return {
            "success": True,
            "title": title,
            "content": content,
            "url": url,
            "error": ""
        }
        
    except requests.Timeout:
        return {"success": False, "title": "", "content": "", "error": "Timeout: No response from server"}
    except requests.RequestException as e:
        return {"success": False, "title": "", "content": "", "error": f"Fetch error: {str(e)}"}
    except Exception as e:
        return {"success": False, "title": "", "content": "", "error": f"Parse error: {str(e)}"}


# --- Dynamic Expertise Extraction ---
def extract_dynamic_expertise(content: str, clients: dict) -> str:
    """
    トピックまたは記事内容から動的に専門性コンテキストを生成
    軽量モデルを使用してコスト節約
    """
    if not content or len(content.strip()) < 10:
        return ""
    
    # 入力を適切な長さに制限
    truncated_content = content[:3000]
    
    extraction_prompt = EXPERTISE_EXTRACTION_PROMPT.format(content=truncated_content)
    
    try:
        # 軽量・高速モデルを優先使用
        if clients.get("google"):
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content(extraction_prompt)
            return response.text.strip()
        elif clients.get("openai"):
            client = clients["openai"]
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.3,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        elif clients.get("anthropic"):
            client = clients["anthropic"]
            response = client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=300,
                temperature=0.3,
                messages=[{"role": "user", "content": extraction_prompt}]
            )
            return response.content[0].text.strip()
    except Exception as e:
        print(f"Expertise extraction failed: {e}")
        return ""
    
    return ""


# --- File Upload Processing Functions ---
def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return filename.split('.')[-1].lower() if '.' in filename else ""


def extract_pdf_text(file_bytes: bytes) -> dict:
    """
    Extract text from PDF
    Returns: {"success": bool, "content": str, "error": str, "pages": int}
    """
    try:
        # Try pdfplumber first (better text extraction)
        if pdfplumber:
            pdf_file = io.BytesIO(file_bytes)
            with pdfplumber.open(pdf_file) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                
                return {
                    "success": True,
                    "content": text.strip(),
                    "error": "",
                    "pages": len(pdf.pages)
                }
        
        # Fallback to PyPDF2
        elif PyPDF2:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n\n"
            
            return {
                "success": True,
                "content": text.strip(),
                "error": "",
                "pages": len(pdf_reader.pages)
            }
        else:
            return {"success": False, "content": "", "error": "PDF processing library not installed", "pages": 0}
            
    except Exception as e:
        return {"success": False, "content": "", "error": f"PDF extraction error: {str(e)}", "pages": 0}


def analyze_csv_excel(file_bytes: bytes, filename: str) -> dict:
    """
    Analyze CSV/Excel file and generate summary
    Returns: {"success": bool, "content": str, "error": str}
    """
    try:
        file_ext = get_file_extension(filename)
        
        # Read file
        if file_ext == "csv":
            df = pd.read_csv(io.BytesIO(file_bytes))
        elif file_ext in ["xlsx", "xls"]:
            df = pd.read_excel(io.BytesIO(file_bytes))
        else:
            return {"success": False, "content": "", "error": "Unsupported file format"}
        
        # Generate summary
        summary = f"""
# Data File Analysis Summary

## Basic Info
- Filename: {filename}
- Rows: {len(df)}
- Columns: {len(df.columns)}

## Column List
{', '.join(df.columns.tolist())}

## Data Preview (First 5 rows)
{df.head().to_string()}

## Statistical Summary
{df.describe().to_string()}

## Data Types
{df.dtypes.to_string()}
"""
        
        return {"success": True, "content": summary, "error": ""}
        
    except Exception as e:
        return {"success": False, "content": "", "error": f"Data analysis error: {str(e)}"}


def analyze_image_with_vision(image_bytes: bytes, clients: dict) -> dict:
    """
    Analyze image using Vision API
    Returns: {"success": bool, "content": str, "error": str}
    """
    try:
        # Try OpenAI GPT-4o (best vision capabilities)
        if clients.get("openai"):
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            response = clients["openai"].chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": VISION_ANALYSIS_PROMPT},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            return {"success": True, "content": response.choices[0].message.content, "error": ""}
        
        # Try Google Gemini (good vision support)
        elif clients.get("google"):
            image = Image.open(io.BytesIO(image_bytes))
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            response = model.generate_content([VISION_ANALYSIS_PROMPT, image])
            return {"success": True, "content": response.text, "error": ""}
        
        # Try Anthropic Claude (vision support)
        elif clients.get("anthropic"):
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            response = clients["anthropic"].messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image,
                                }
                            },
                            {
                                "type": "text",
                                "text": VISION_ANALYSIS_PROMPT
                            }
                        ]
                    }
                ]
            )
            return {"success": True, "content": response.content[0].text, "error": ""}
        
        else:
            return {"success": False, "content": "", "error": "Vision API not available (OpenAI/Google/Anthropic API key required)"}
            
    except Exception as e:
        return {"success": False, "content": "", "error": f"Image analysis error: {str(e)}"}


def process_uploaded_file(uploaded_file, clients: dict) -> dict:
    """
    Process uploaded file and extract content
    Returns: {"success": bool, "content": str, "error": str, "file_info": dict}
    """
    file_bytes = uploaded_file.read()
    filename = uploaded_file.name
    file_ext = get_file_extension(filename)
    file_size_mb = len(file_bytes) / (1024 * 1024)
    
    # Check file size
    max_size = FILE_UPLOAD_CONFIG.get("max_file_size_mb", 10)
    if file_size_mb > max_size:
        return {
            "success": False,
            "content": "",
            "error": f"File size too large ({file_size_mb:.1f}MB > {max_size}MB)",
            "file_info": {}
        }
    
    # Check extension
    allowed_exts = FILE_UPLOAD_CONFIG.get("allowed_extensions", {})
    if file_ext not in allowed_exts:
        return {
            "success": False,
            "content": "",
            "error": f"Unsupported file format: .{file_ext}",
            "file_info": {}
        }
    
    file_info = {
        "name": filename,
        "extension": file_ext,
        "size_mb": file_size_mb,
        "icon": allowed_exts[file_ext]["icon"]
    }
    
    # Process based on file type
    if file_ext == "pdf":
        result = extract_pdf_text(file_bytes)
        result["file_info"] = file_info
        return result
    
    elif file_ext in ["csv", "xlsx", "xls"]:
        result = analyze_csv_excel(file_bytes, filename)
        result["file_info"] = file_info
        return result
    
    elif file_ext in ["png", "jpg", "jpeg"]:
        result = analyze_image_with_vision(file_bytes, clients)
        result["file_info"] = file_info
        return result
    
    elif file_ext in ["txt", "md"]:
        try:
            content = file_bytes.decode('utf-8')
            return {
                "success": True,
                "content": content,
                "error": "",
                "file_info": file_info
            }
        except Exception as e:
            return {
                "success": False,
                "content": "",
                "error": f"Text reading error: {str(e)}",
                "file_info": file_info
            }
    
    return {
        "success": False,
        "content": "",
        "error": "Unsupported file format",
        "file_info": file_info
    }


# --- AI Call Function ---
def ask_ai(model_name: str, clients: dict, history_text: str, is_first: bool = False, 
           topic: str = "", temperature: float = 0.7, expertise: str = "General",
           personality: str = None, url_content: dict = None, 
           file_content: list = None,  # Now accepts list of file results
           dynamic_expertise: str = None) -> str:
    provider, model_id = ALL_MODELS[model_name]
    system_prompt = get_system_prompt(expertise, personality, dynamic_expertise)
    
    # File content integration (highest priority) - now handles list
    if file_content and len(file_content) > 0:
        # Build combined file context
        file_summaries = []
        combined_content = []
        
        for f in file_content:
            if f.get("success"):
                file_info = f.get("file_info", {})
                file_summaries.append(f"- {file_info.get('icon', '')} {file_info.get('name', 'unknown')} ({file_info.get('extension', '').upper()})")
                combined_content.append(f"[{file_info.get('name', 'unknown')}]\n{f['content'][:4000]}")
        
        if combined_content:
            file_context = f"""
**Context: Analyzing Uploaded Files**
You are analyzing content from {len(combined_content)} uploaded file(s).
The user's question/instruction is: "{topic}"

**Files:**
{chr(10).join(file_summaries)}

**File Contents:**
{chr(10).join(combined_content)[:8000]}

Focus your discussion on the file contents while addressing the user's question.
"""
            system_prompt = system_prompt + "\n" + file_context
    
    # URL content integration (if no file)
    elif url_content and url_content.get("success"):
        url_context = URL_ANALYSIS_PROMPT_ADDITION.format(
            article_content=url_content["content"][:6000],
            url=url_content.get("url", "")
        )
        system_prompt = system_prompt + "\n" + url_context

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
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }
            if model_id not in NO_TEMPERATURE_MODELS:
                params["temperature"] = temperature
            response = clients["openai"].chat.completions.create(**params)
            return response.choices[0].message.content

        elif provider == "anthropic":
            if not clients["anthropic"]:
                return "❌ Anthropic API key not configured"
            response = clients["anthropic"].messages.create(
                model=model_id,
                max_tokens=1500,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text

        elif provider == "google":
            if not clients["google"]:
                return "❌ Google API key not configured"
            model = genai.GenerativeModel(model_id, generation_config={"temperature": temperature})
            full_prompt = f"{system_prompt}\n\n{prompt}"
            response = model.generate_content(full_prompt)
            return response.text

    except Exception as e:
        return f"❌ Error ({model_name}): {e}"


# --- Facilitator Function ---
def facilitate(facilitator_name: str, clients: dict, topic: str, full_log: str, collaborators: list, expertise: str = "General", synthesis_format: str = "default") -> str:
    provider, model_id = ALL_MODELS[facilitator_name]

    collab_list = "\n".join([f"- **{c}**" for c in collaborators])
    facilitator_prompt = get_facilitator_prompt_by_format(synthesis_format, expertise).format(topic=topic, collaborator_list=collab_list)
    
    # Compress log for long discussions to avoid token limits
    # Estimate: ~4 chars per token, keep under 8000 tokens for log
    max_log_chars = 32000
    if len(full_log) > max_log_chars:
        # Keep first 25% and last 75% of discussion
        split_point = len(full_log) // 4
        compressed_log = full_log[:split_point] + "\n\n[... middle discussion compressed ...]\n\n" + full_log[-split_point*3:]
        full_prompt = f"{facilitator_prompt}\n\n--- Discussion Log (Compressed) ---\n{compressed_log}"
    else:
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
                max_tokens=4000,  # Increased for longer syntheses
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
if "generating" not in st.session_state:
    st.session_state.generating = False
if "discussion_history" not in st.session_state:
    st.session_state.discussion_history = []
if "current_topic" not in st.session_state:
    st.session_state.current_topic = None
if "current_participants" not in st.session_state:
    st.session_state.current_participants = []
# Personality system
if "personality_assignments" not in st.session_state:
    st.session_state.personality_assignments = {}
if "personality_mode" not in st.session_state:
    st.session_state.personality_mode = "auto"
# URL reading
if "url_content" not in st.session_state:
    st.session_state.url_content = None
if "detected_url" not in st.session_state:
    st.session_state.detected_url = None
# Dynamic expertise
if "dynamic_expertise" not in st.session_state:
    st.session_state.dynamic_expertise = None
# File upload (multiple files support)
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []  # List of file results
if "uploaded_file_names" not in st.session_state:
    st.session_state.uploaded_file_names = set()  # Set of uploaded file names
# Form key for reset
if "form_key" not in st.session_state:
    st.session_state.form_key = 0
# Loop tracking for rerun protection
if "loop_in_progress" not in st.session_state:
    st.session_state.loop_in_progress = False
if "loop_current_round" not in st.session_state:
    st.session_state.loop_current_round = 0
if "loop_current_model" not in st.session_state:
    st.session_state.loop_current_model = 0
if "loop_config" not in st.session_state:
    st.session_state.loop_config = None
if "history_log" not in st.session_state:
    st.session_state.history_log = []
# Re-discussion context
if "rediscuss_context" not in st.session_state:
    st.session_state.rediscuss_context = None
# Auto-start rediscuss flag
if "auto_start_rediscuss" not in st.session_state:
    st.session_state.auto_start_rediscuss = None
# Previous synthesis for display in expander
if "previous_synthesis_for_display" not in st.session_state:
    st.session_state.previous_synthesis_for_display = None

# --- Authentication Gate ---
# --- Main Layout ---
# Display Logo
logo_base64 = get_logo_base64()
if logo_base64:
    st.markdown(f'''
    <div class="logo-container">
        <img src="data:image/png;base64,{logo_base64}" alt="X-Think Logo">
    </div>
    ''', unsafe_allow_html=True)
else:
    st.title("✦ X-Think AI Idea Lab")

# Three-column layout
col_config, col_main, col_synthesis = st.columns([3, 4, 3], gap="medium")

# --- LEFT COLUMN: Configuration (all inside a collapsible expander) ---
with col_config:
    st.markdown("### ✦ Configuration")
    with st.expander("", expanded=True):
        # API Status
        st.markdown('<p class="section-header">API Keys</p>', unsafe_allow_html=True)
        for provider, is_set in api_status.items():
            if is_set:
                st.markdown(f'<div class="api-badge connected">✓ {provider.upper()}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="api-badge disconnected">✗ {provider.upper()}</div>', unsafe_allow_html=True)

        # Model Selection - OpenAI
        st.markdown('<p class="section-header">AI Collaborators</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.9rem; color: #888;">OpenAI</p>', unsafe_allow_html=True)
        selected_openai = st.multiselect(
            "OpenAI Models",
            list(OPENAI_MODELS.keys()),
            default=["GPT-4o"] if api_status["openai"] else [],
            disabled=not api_status["openai"],
            label_visibility="collapsed"
        )

        # Model Selection - Anthropic
        st.markdown('<p style="font-size: 0.9rem; color: #888;">Anthropic</p>', unsafe_allow_html=True)
        selected_anthropic = st.multiselect(
            "Anthropic Models",
            list(ANTHROPIC_MODELS.keys()),
            default=["Claude Haiku 4.5"] if api_status["anthropic"] else [],
            disabled=not api_status["anthropic"],
            label_visibility="collapsed"
        )

        # Model Selection - Google
        st.markdown('<p style="font-size: 0.9rem; color: #888;">Google</p>', unsafe_allow_html=True)
        selected_google = st.multiselect(
            "Google Models",
            list(GOOGLE_MODELS.keys()),
            default=["Gemini 2.5 Flash"] if api_status["google"] else [],
            disabled=not api_status["google"],
            label_visibility="collapsed"
        )

        selected_models = selected_openai + selected_anthropic + selected_google

        # Facilitator Selection
        st.markdown('<p class="section-header">Facilitator</p>', unsafe_allow_html=True)
        available_facilitators = []
        for m, (provider, _) in ALL_MODELS.items():
            if m not in selected_models and api_status.get(provider, False):
                available_facilitators.append(m)

        if available_facilitators:
            default_index = 0
            if DEFAULT_FACILITATOR in available_facilitators:
                default_index = available_facilitators.index(DEFAULT_FACILITATOR)
            
            facilitator = st.selectbox(
                "Summary Host", 
                available_facilitators, 
                index=default_index,
                label_visibility="collapsed"
            )
        else:
            st.warning("⚠️ Please keep at least one model available")
            facilitator = None

        # Settings
        st.markdown('<p class="section-header">Settings</p>', unsafe_allow_html=True)
        rounds = st.slider("Number of Rounds", 1, 5, 2, help="Recommended: 2-3 rounds")
        creativity = st.slider("Creativity", 0.0, 1.0, 0.7, 0.1)
        expertise_level = st.select_slider(
            "Expertise Level",
            options=["Beginner", "General", "Professional", "Expert"],
            value="General"
        )
        
        # Synthesis Report Format
        st.markdown('<p class="section-header">Report Format</p>', unsafe_allow_html=True)
        synthesis_format = st.selectbox(
            "Synthesis Report Format",
            options=list(SYNTHESIS_FORMATS.keys()),
            format_func=lambda x: SYNTHESIS_FORMATS[x],
            index=0,
            label_visibility="collapsed"
        )
        
        # Personality settings
        st.markdown('<p class="section-header">AI Personality</p>', unsafe_allow_html=True)
        personality_mode = st.radio(
            "Personality Mode",
            options=list(PERSONALITY_MODES.keys()),
            format_func=lambda x: PERSONALITY_MODES[x],
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.personality_mode = personality_mode
        
        # Manual personality assignment
        if personality_mode == "manual" and selected_models:
            for model in selected_models:
                personality_options = [(pid, f'{pinfo["emoji"]} {pinfo["name_ja"]}') 
                                       for pid, pinfo in AI_PERSONALITIES.items()]
                selected_personality = st.selectbox(
                    f"{model}",
                    options=[p[0] for p in personality_options],
                    format_func=lambda x: next(p[1] for p in personality_options if p[0] == x),
                    key=f"personality_{model}"
                )
                st.session_state.personality_assignments[model] = selected_personality

# --- MIDDLE COLUMN: Main Interaction ---
with col_main:
    st.markdown("### ✦ Topic & Discussion")
    
    # File uploader with multi-file support
    max_files = FILE_UPLOAD_CONFIG.get("max_files", 5)
    max_total_mb = FILE_UPLOAD_CONFIG.get("max_total_size_mb", 30)
    current_file_count = len(st.session_state.uploaded_files_list)
    current_total_mb = sum(f["file_info"]["size_mb"] for f in st.session_state.uploaded_files_list)
    
    # Show current files
    if st.session_state.uploaded_files_list:
        st.markdown(f"**📎 アップロード済み ({current_file_count}/{max_files}ファイル, {current_total_mb:.1f}/{max_total_mb}MB)**")
        
        for idx, file_result in enumerate(st.session_state.uploaded_files_list):
            file_info = file_result["file_info"]
            col_file, col_delete = st.columns([5, 1])
            with col_file:
                st.markdown(f"{file_info['icon']} **{file_info['name']}** ({file_info['size_mb']:.1f}MB)")
            with col_delete:
                if st.button("🗑️", key=f"delete_file_{idx}", help="削除"):
                    st.session_state.uploaded_files_list.pop(idx)
                    st.session_state.uploaded_file_names.discard(file_info['name'])
                    st.rerun()
    
    # File uploader (disabled if limit reached)
    can_upload = current_file_count < max_files
    
    if can_upload:
        uploaded_file = st.file_uploader(
            f"📎 ファイル追加 (残り{max_files - current_file_count})",
            type=list(FILE_UPLOAD_CONFIG["allowed_extensions"].keys()),
            help=f"PDF, CSV, Excel, 画像をアップロード (上限: {max_files}ファイル, 合計{max_total_mb}MB)",
            key=f"file_uploader_{st.session_state.form_key}_{current_file_count}"
        )
        
        # Process uploaded file
        if uploaded_file is not None:
            # Check if already uploaded
            if uploaded_file.name not in st.session_state.uploaded_file_names:
                # Check total size limit
                file_size_mb = len(uploaded_file.read()) / (1024 * 1024)
                uploaded_file.seek(0)
                
                if current_total_mb + file_size_mb > max_total_mb:
                    st.error(f"❌ 合計サイズ上限超過 ({current_total_mb + file_size_mb:.1f}MB > {max_total_mb}MB)")
                else:
                    with st.spinner(f"📄 Processing {uploaded_file.name}..."):
                        clients = init_clients()
                        file_result = process_uploaded_file(uploaded_file, clients)
                        
                        if file_result["success"]:
                            st.session_state.uploaded_files_list.append(file_result)
                            st.session_state.uploaded_file_names.add(uploaded_file.name)
                            st.success(f"✅ 追加: {file_result['file_info']['icon']} {file_result['file_info']['name']}")
                            st.rerun()
                        else:
                            st.error(f"❌ {file_result['error']}")
    else:
        st.info(f"📎 ファイル上限に達しました ({max_files}ファイル)")

    
    
    with st.form(key=f"session_form_{st.session_state.form_key}"):
        topic = st.text_area(
            "Topic",
            "",
            height=100,
            label_visibility="collapsed",
            placeholder="Enter your topic...\n💡 Paste a URL to automatically fetch and discuss article content"
        )
        start_button = st.form_submit_button("✦ Start Session", type="primary", use_container_width=True)

    # Validation (show warnings outside form)
    can_start = True
    if start_button:
        if not topic.strip():
            st.warning("⚠️ Please enter a topic")
            can_start = False
        if len(selected_models) < 2:
            st.warning("⚠️ Please select at least 2 AI collaborators")
            can_start = False
        if not facilitator:
            st.warning("⚠️ Please select a facilitator")
            can_start = False

    # Chat history display area
    chat_container = st.container()

# --- RIGHT COLUMN: Synthesis Canvas ---
with col_synthesis:
    st.markdown("### ✦ Synthesis")
    synthesis_container = st.container()

# --- Display Previous Discussion (if exists) ---
with chat_container:
    if st.session_state.discussion_history:
        st.markdown("---")
        st.markdown(f"**Topic:** {st.session_state.current_topic}")
        
        # Show previous synthesis in expander if available
        st.markdown(f"**Participants:** {', '.join(st.session_state.current_participants)}")
        st.markdown(f"**Facilitator:** {st.session_state.facilitator_name}")
        st.markdown("---")
        
        for msg in st.session_state.discussion_history:
            with st.chat_message("assistant", avatar=msg["avatar"]):
                # Display personality badge if available
                if "personality_info" in msg and msg["personality_info"]:
                    pinfo = msg["personality_info"]
                    st.markdown(
                        f'<span class="model-badge">{msg["model"]}</span> '
                        f'<span class="personality-badge" style="background: {pinfo["color"]}20; '
                        f'color: {pinfo["color"]}; border: 1px solid {pinfo["color"]}40;">'
                        f'{pinfo["emoji"]} {pinfo["name_ja"]}</span>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(f'<span class="model-badge">{msg["model"]}</span>', unsafe_allow_html=True)
                st.write(msg["content"])

# --- Run Session ---
def assign_personalities(models: list, mode: str) -> dict:
    """Assign personalities to models based on mode"""
    import random
    assignments = {}
    personality_ids = get_all_personality_ids()
    
    if mode == "auto":
        # Cycle through personalities for balanced discussion
        for i, model in enumerate(models):
            assignments[model] = personality_ids[i % len(personality_ids)]
    elif mode == "random":
        for model in models:
            assignments[model] = random.choice(personality_ids)
    elif mode == "manual":
        # Use session state assignments
        assignments = st.session_state.personality_assignments.copy()
        # Fill in any missing assignments
        for model in models:
            if model not in assignments:
                assignments[model] = personality_ids[0]
    
    return assignments

# Start new session or continue interrupted one
should_run_loop = False

if start_button and can_start:
    # New session - clear and initialize
    st.session_state.discussion_history = []
    st.session_state.history_log = []
    st.session_state.current_topic = topic
    st.session_state.current_participants = selected_models
    st.session_state.loop_in_progress = True
    st.session_state.loop_current_round = 0
    st.session_state.loop_current_model = 0
    
    # Save loop config for rerun continuation
    st.session_state.loop_config = {
        "topic": topic,
        "rounds": rounds,
        "selected_models": selected_models,
        "facilitator": facilitator,
        "creativity": creativity,
        "expertise_level": expertise_level,
        "synthesis_format": synthesis_format
    }
    
    
    # Assign personalities
    st.session_state.personality_assignments = assign_personalities(
        selected_models, 
        st.session_state.personality_mode
    )
    current_assignments = st.session_state.personality_assignments
    
    # URL Detection and Content Fetching
    detected_url = detect_url(topic)
    url_content_data = None
    
    if detected_url:
        with st.spinner(f"🌐 Loading article... {detected_url[:50]}..."):
            url_content_data = fetch_url_content(detected_url)
            
            if url_content_data["success"]:
                st.success(f"✅ Article fetched: {url_content_data['title'][:50]}...")
                st.session_state.url_content = url_content_data
                st.session_state.detected_url = detected_url
                
                # Show article preview
                with st.expander("📄 Article Content (Preview)", expanded=False):
                    st.markdown(f"**Title:** {url_content_data['title']}")
                    st.markdown(f"**URL:** {detected_url}")
                    st.text(url_content_data['content'][:1000] + "...")
            else:
                st.warning(f"⚠️ Failed to fetch article: {url_content_data['error']}")
                st.info("💡 Continuing discussion as text without URL")
    
    clients = init_clients()
    
    # Dynamic Expertise Extraction
    # Content Source Priority: File > URL > Topic
    content_to_analyze = ""
    content_source = "topic"
    
    if st.session_state.uploaded_files_list:
        # Combine all file contents
        combined_content = "\n\n---\n\n".join([
            f"[{f['file_info']['name']}]\n{f['content'][:3000]}"
            for f in st.session_state.uploaded_files_list
        ])
        content_to_analyze = combined_content
        content_source = "file"
    elif url_content_data and url_content_data.get("success"):
        # URL has second priority
        content_to_analyze = url_content_data["content"]
        content_source = "url"
    else:
        # Topic text as fallback
        content_to_analyze = topic
        content_source = "topic"
    
    with st.spinner("🎓 Analyzing required expertise..."):
        dynamic_expertise = extract_dynamic_expertise(content_to_analyze, clients)
        st.session_state.dynamic_expertise = dynamic_expertise
        
        if dynamic_expertise:
            with st.expander("🎓 Auto-detected Expertise", expanded=False):
                st.markdown(dynamic_expertise)
    
    history_log = []
    st.session_state.generating = True

    with chat_container:
        st.markdown("---")
        st.markdown(f"**Topic:** {st.session_state.current_topic}")
        
        # Show content source
        if st.session_state.uploaded_files_list:
            file_names = ", ".join([f["file_info"]["icon"] + " " + f["file_info"]["name"] for f in st.session_state.uploaded_files_list])
            st.markdown(f"**📎 Files:** {file_names}")
        elif detected_url and url_content_data and url_content_data.get("success"):
            st.markdown(f"**📰 Article:** {url_content_data['title'][:60]}...")
        
        st.markdown(f"**Participants:** {', '.join(selected_models)}")
        st.markdown(f"**Facilitator:** {facilitator}")
        
        if st.session_state.dynamic_expertise:
            st.markdown(f"**🎓 Expertise:** {st.session_state.dynamic_expertise[:100]}...")
        
        st.markdown("---")

        # Progress tracking - use simple counter instead of st.empty()
        total_calls = rounds * len(selected_models)
        progress_bar = st.progress(0)
        current_call = 0

        # Collaboration Phase
        try:
            for i in range(rounds):
                st.markdown(f'<span class="round-badge">Round {i+1}/{rounds}</span>', unsafe_allow_html=True)

                for j, model in enumerate(selected_models):
                    current_call += 1
                    progress = current_call / total_calls
                    progress_bar.progress(progress)
                    
                    # Get personality for this model
                    personality = current_assignments.get(model)
                    personality_info = get_personality_info(personality)
                    
                    # Removed status_text.text() to reduce UI updates
                    
                    with st.chat_message("assistant", avatar=get_personality_avatar(personality, model)):
                        # Display model name and personality badge
                        st.markdown(
                            f'<span class="model-badge">{model}</span> '
                            f'<span class="personality-badge" style="background: {personality_info["color"]}20; '
                            f'color: {personality_info["color"]}; border: 1px solid {personality_info["color"]}40;">'
                            f'{personality_info["emoji"]} {personality_info["name_ja"]}</span>',
                            unsafe_allow_html=True
                        )

                        # Retry logic for API calls
                        max_retries = 2
                        retry_count = 0
                        msg = None
                        
                        while retry_count <= max_retries and msg is None:
                            try:
                                if i == 0 and j == 0:
                                    msg = ask_ai(model, clients, "", is_first=True, topic=topic, 
                                                 temperature=creativity, expertise=expertise_level,
                                                 personality=personality, url_content=url_content_data,
                                                 file_content=st.session_state.uploaded_files_list,
                                                 dynamic_expertise=st.session_state.dynamic_expertise)
                                else:
                                    # Dynamic context window: fewer messages for longer discussions
                                    context_window = max(3, min(6, 20 // rounds))
                                    context_text = "\n\n".join(history_log[-context_window:])
                                    msg = ask_ai(model, clients, context_text, 
                                                 temperature=creativity, expertise=expertise_level,
                                                 personality=personality, url_content=url_content_data,
                                                 file_content=st.session_state.uploaded_files_list,
                                                 dynamic_expertise=st.session_state.dynamic_expertise)
                                
                                # Check if the response is an error message
                                if msg and msg.startswith("❌"):
                                    if retry_count < max_retries:
                                        st.warning(f"⚠️ Retry {retry_count + 1}/{max_retries} for {model}...")
                                        time.sleep(2)
                                        retry_count += 1
                                        msg = None
                                    else:
                                        st.error(f"Failed after {max_retries} retries: {msg}")
                                else:
                                    break
                            except Exception as e:
                                if retry_count < max_retries:
                                    st.warning(f"⚠️ Error occurred, retrying... ({retry_count + 1}/{max_retries})")
                                    time.sleep(2)
                                    retry_count += 1
                                else:
                                    msg = f"❌ Error after {max_retries} retries: {str(e)}"
                                    st.error(msg)
                                    break

                        if msg:
                            st.write(msg)
                            history_log.append(f"[{model} ({personality_info['name_ja']})]: {msg}")
                            # Store in session state for persistence
                            st.session_state.discussion_history.append({
                                "model": model,
                                "content": msg,
                                "avatar": get_personality_avatar(personality, model),
                                "personality": personality,
                                "personality_info": personality_info
                            })
                        else:
                            error_msg = f"❌ {model} failed to respond"
                            st.error(error_msg)
                            history_log.append(f"[{model}]: {error_msg}")

            progress_bar.progress(1.0)
            st.success("✦ Discussion complete! Generating summary...")
            
        except Exception as e:
            st.error(f"❌ Session error: {str(e)}")
            st.warning("⚠️ Partial results may be available. Attempting to generate summary...")


    # Update Canvas with results
    full_log = "\n\n".join(history_log)

    # Show progress in synthesis column during summary generation
    with synthesis_container:
        synthesis_progress = st.empty()
        synthesis_progress.markdown(f"""
        <div class="canvas-card">
            <h2 class="report-title">✦ Idea Synthesis Report</h2>
            <div class="generating-spinner"></div>
            <p style="text-align: center; margin-top: 1rem;">🤖 {facilitator} is analyzing the discussion...</p>
            <p style="text-align: center; color: var(--text-secondary); font-size: 0.9rem;">This may take 30-60 seconds for long discussions</p>
            <p style="text-align: center; color: var(--text-secondary); font-size: 0.8rem; margin-top: 0.5rem;">Log length: {len(full_log)} chars</p>
        </div>
        """, unsafe_allow_html=True)

    # Generate summary (this happens while chat logs remain visible)
    conclusion = None
    try:
        import time
        start_time = time.time()
        conclusion = facilitate(facilitator, clients, topic, full_log, selected_models, expertise=expertise_level, synthesis_format=synthesis_format)
        elapsed = time.time() - start_time
        
        # Check if conclusion is actually an error message
        if conclusion and conclusion.startswith("❌"):
            raise Exception(f"Facilitator returned error: {conclusion}")
            
    except Exception as e:
        elapsed = time.time() - start_time if 'start_time' in locals() else 0
        error_msg = str(e)
        
        # Provide detailed error information
        conclusion = f"""❌ **Synthesis Error** (after {elapsed:.1f}s)

**Error:** {error_msg}

**Troubleshooting:**
- Try using a different facilitator model
- Reduce the number of rounds
- Check API key status

**Discussion Summary Available:**
The discussion log is preserved above. You can manually review the {len(history_log)} messages exchanged.
"""
        
        with synthesis_container:
            synthesis_progress.empty()
            st.error(f"Failed to generate synthesis after {elapsed:.1f}s: {error_msg}")
            st.info("💡 Tip: Try GPT-4o or Claude Sonnet 4 as facilitator for better reliability")

    # Clear the progress indicator
    if conclusion and not conclusion.startswith("❌"):
        synthesis_progress.empty()

    # Save to session state
    st.session_state.conclusion = conclusion
    st.session_state.facilitator_name = facilitator
    st.session_state.full_report = f"Topic: {topic}\n\n{full_log}\n\n--- Summary ---\n{conclusion}"
    st.session_state.generating = False

    show_star_celebration()
    # Don't rerun - let the synthesis display below handle it

# --- Synthesis Display ---
with synthesis_container:
    if st.session_state.conclusion:
        st.markdown('<h3 class="report-title">✦ Idea Synthesis Report</h3>', unsafe_allow_html=True)
        with st.chat_message("assistant", avatar=get_avatar(st.session_state.facilitator_name)):
            st.markdown(f'<span class="model-badge">{st.session_state.facilitator_name}</span>', unsafe_allow_html=True)
            st.markdown(st.session_state.conclusion)

        # --- Download Options (Multiple Formats) ---
        st.markdown('<p class="section-header">Download Report</p>', unsafe_allow_html=True)
        
        # Prepare data for different formats
        topic = st.session_state.current_topic or "Untitled"
        discussion = st.session_state.discussion_history or []
        summary = st.session_state.conclusion or ""
        facilitator = st.session_state.facilitator_name or "Unknown"
        
        # Generate filenames
        import re
        safe_topic = re.sub(r'[^\w\s-]', '', topic[:30]).strip().replace(' ', '_') or 'report'
        
        # TXT format (original)
        txt_content = st.session_state.full_report
        
        # Markdown format
        md_content = f"""# X-Think Idea Synthesis Report

## Topic
{topic}

## Discussion Summary
**Facilitator:** {facilitator}

{summary}

## Discussion History
"""
        for i, msg in enumerate(discussion, 1):
            md_content += f"\n### Round {i}: {msg.get('model', 'Unknown')}\n"
            if msg.get('personality'):
                md_content += f"*Personality: {msg['personality']}*\n\n"
            md_content += f"{msg.get('content', '')}\n"
        
        # JSON format
        import json
        json_data = {
            "topic": topic,
            "facilitator": facilitator,
            "summary": summary,
            "discussion_history": [
                {
                    "round": i,
                    "model": msg.get("model", "Unknown"),
                    "personality": msg.get("personality", ""),
                    "content": msg.get("content", "")
                }
                for i, msg in enumerate(discussion, 1)
            ],
            "metadata": {
                "generated_by": "X-Think",
                "timestamp": __import__('datetime').datetime.now().isoformat()
            }
        }
        json_content = json.dumps(json_data, ensure_ascii=False, indent=2)
        
        # HTML format
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>X-Think Report: {topic[:50]}</title>
    <style>
        body {{ font-family: 'Inter', sans-serif; max-width: 800px; margin: 0 auto; padding: 2rem; background: #1a1a1a; color: #f0f0f0; }}
        h1 {{ color: #D4AF37; border-bottom: 2px solid #D4AF37; padding-bottom: 0.5rem; }}
        h2 {{ color: #D4AF37; }}
        .summary {{ background: #2a2a2a; padding: 1.5rem; border-radius: 8px; border-left: 4px solid #D4AF37; }}
        .message {{ background: #252525; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
        .model {{ color: #D4AF37; font-weight: bold; }}
        .personality {{ color: #888; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>✦ X-Think Idea Synthesis Report</h1>
    <h2>Topic</h2>
    <p>{topic}</p>
    <h2>Summary</h2>
    <div class="summary">
        <p><strong>Facilitator:</strong> {facilitator}</p>
        <div>{summary.replace(chr(10), '<br>')}</div>
    </div>
    <h2>Discussion History</h2>
"""
        for i, msg in enumerate(discussion, 1):
            html_content += f"""    <div class="message">
        <p class="model">Round {i}: {msg.get('model', 'Unknown')}</p>
        {"<p class='personality'>Personality: " + msg.get('personality', '') + "</p>" if msg.get('personality') else ""}
        <p>{msg.get('content', '').replace(chr(10), '<br>')}</p>
    </div>
"""
        html_content += """</body>
</html>"""
        
        # CSV format
        import csv
        import io
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Round", "Model", "Personality", "Content"])
        for i, msg in enumerate(discussion, 1):
            writer.writerow([i, msg.get("model", ""), msg.get("personality", ""), msg.get("content", "")])
        writer.writerow([])
        writer.writerow(["Summary", facilitator, "", summary])
        csv_content = csv_buffer.getvalue()
        
        # Download buttons in columns (5 formats)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.download_button("TXT", txt_content, f"{safe_topic}.txt", use_container_width=True)
        with col2:
            st.download_button("MD", md_content, f"{safe_topic}.md", use_container_width=True)
        with col3:
            st.download_button("JSON", json_content, f"{safe_topic}.json", mime="application/json", use_container_width=True)
        with col4:
            st.download_button("HTML", html_content, f"{safe_topic}.html", mime="text/html", use_container_width=True)
        with col5:
            st.download_button("CSV", csv_content, f"{safe_topic}.csv", mime="text/csv", use_container_width=True)

        if st.button("✦ Reset", use_container_width=True):
            # Full reset - clear everything
            st.session_state.conclusion = None
            st.session_state.facilitator_name = None
            st.session_state.full_report = None
            st.session_state.rediscuss_context = None
            st.session_state.discussion_history = []
            st.session_state.current_topic = None
            st.session_state.generating = False
            st.session_state.url_content = None
            st.session_state.detected_url = None
            st.session_state.uploaded_files_list = []
            st.session_state.uploaded_file_names = set()
            st.session_state.dynamic_expertise = None
            # Increment form key to reset text area
            st.session_state.form_key += 1
            st.rerun()


    elif st.session_state.generating:
        st.markdown("""
        <div class="canvas-card">
            <h2 class="report-title">✦ Idea Synthesis Report</h2>
            <div class="generating-spinner"></div>
            <p>Synthesizing discussion...</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="canvas-card">
            <h2 class="report-title">✦ Idea Synthesis Report</h2>
            <p>Start a session to see the AI-generated summary here</p>
        </div>
        """, unsafe_allow_html=True)
