"""
AI Idea Lab - Configuration Module
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file (override existing environment variables)
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path, override=True)


def _get_api_key(key_name: str) -> str:
    """Get API key (Streamlit Cloud compatible)"""
    # Try Streamlit Secrets first
    try:
        import streamlit as st
        if hasattr(st, 'secrets') and key_name in st.secrets:
            return st.secrets[key_name]
    except Exception:
        pass
    # Fall back to environment variables
    return os.getenv(key_name, "")


# --- API Keys ---
OPENAI_API_KEY = _get_api_key("OPENAI_API_KEY")
ANTHROPIC_API_KEY = _get_api_key("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = _get_api_key("GOOGLE_API_KEY")

# --- Model Definitions ---
# Models that don't support temperature parameter
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

# All models list (provider, model_id)
ALL_MODELS = {}
ALL_MODELS.update({k: ("openai", v) for k, v in OPENAI_MODELS.items()})
ALL_MODELS.update({k: ("anthropic", v) for k, v in ANTHROPIC_MODELS.items()})
ALL_MODELS.update({k: ("google", v) for k, v in GOOGLE_MODELS.items()})

# --- Prompts ---
SYSTEM_PROMPT = """
You are a brainstorming expert who expands ideas creatively.

**CRITICAL: Language Rule**
You MUST respond in the SAME LANGUAGE as the topic provided. If the topic is in Japanese, respond in Japanese. If in Chinese, respond in Chinese. If in English, respond in English. Match the language exactly.

**Your Role:**
You are participating in a collaborative discussion. Build upon or respond to the previous speaker's idea while adding your own unique perspective.

**How to Engage:**
1. First, briefly acknowledge or reference something from the previous comment (agree, disagree, extend, or question it)
2. Then, add your own new angle using one of these approaches:
   - **Different Perspective** - How would this look from another viewpoint?
   - **Cross-pollination** - What if we combined this with an unrelated field?
   - **Constructive Challenge** - What potential issue do you see, and how might we address it?
   - **Scale Shift** - What if we made it much smaller or much larger?
   - **Build & Extend** - Take their idea further in a new direction

**Rules:**
- Always connect your comment to the previous one (e.g., "Building on that...", "That raises an interesting point, but...", "Taking that idea further...")
- Don't use excessive praise like "Great idea!" - just engage naturally
- Include one concrete example
- Keep the discussion flowing like a real conversation

**Output Format:**
3-5 sentences that respond to the previous comment AND add something new.
"""

FACILITATOR_PROMPT = """
You are a strategic facilitator who synthesizes discussions into actionable outcomes.

**CRITICAL: Language Rule**
You MUST write in the SAME LANGUAGE as the topic provided. If Japanese, write in Japanese. If Chinese, write in Chinese. Match exactly.

Your job is NOT just to summarize - you must SYNTHESIZE the discussion into a coherent, actionable conclusion.

---

## Conclusion

### The Core Idea
Synthesize all perspectives into ONE unified concept. Don't just list what was said - combine the best elements into a single, powerful idea. (2-3 sentences)

### Why This Works
Explain how the different perspectives complement each other and why this combined approach is stronger than any single idea. (2-3 sentences)

### Concrete Proposal
Based on the discussion, propose a specific, implementable solution:

**What:** Describe the solution in detail
**Who:** Who should lead this? Who benefits?
**How:** 3-5 specific steps to implement, in order of priority
**When:** Suggest a realistic timeline (immediate/short-term/long-term actions)

### Key Insights from Discussion
{collaborator_list}
One key contribution from each participant that shaped the final conclusion.

### Potential Challenges & Mitigations
Identify 2-3 potential obstacles and how to address them.

---
Topic: {topic}
"""


def get_avatar(model_name: str) -> str:
    """Get avatar emoji from model name"""
    if any(k in model_name for k in ["GPT", "o3", "o4"]):
        return "🟢"
    elif "Claude" in model_name:
        return "🟣"
    elif "Gemini" in model_name:
        return "🔵"
    return "⚪"


def check_api_keys() -> dict:
    """Check API key status"""
    return {
        "openai": bool(OPENAI_API_KEY and not OPENAI_API_KEY.startswith("sk-xxxx")),
        "anthropic": bool(ANTHROPIC_API_KEY and not ANTHROPIC_API_KEY.startswith("sk-ant-xxxx")),
        "google": bool(GOOGLE_API_KEY and not GOOGLE_API_KEY.startswith("AIzaxxxx")),
    }
