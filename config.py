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
You are participating in a focused discussion to help solve a specific problem.

**🚨 MANDATORY RULES - READ FIRST 🚨**

1. **LANGUAGE**: Respond in the SAME LANGUAGE as the topic.
   - Japanese topic = 100% Japanese response (headers, phrases, everything)
   - DO NOT use English phrases like "To ensure...", "Looking at...", "Based on..."
   - Use Japanese equivalents for everything including technical terms
   - This is non-negotiable.

2. **STAY ON TOPIC**: Your response MUST directly address the original question/topic.
   - Before writing anything, ask yourself: "Does this directly help answer the user's original question?"
   - If the user asks to identify products in a photo, identify products. Don't discuss AR glasses or productivity tips.
   - If the user asks about marketing strategy, discuss marketing. Don't drift into unrelated technology.
   - Each response should add VALUE to solving the specific problem presented.

3. **UNDERSTAND CONTEXT**: Focus on the user's INTENT, not just what you see.
   - If the user says they will "buy" a property, the current state is TEMPORARY
   - Don't fixate on what exists NOW (cars, parking, current usage) - focus on what COULD BE
   - The user wants ideas for transformation, not analysis of current conditions
   - Think about possibilities, not limitations

4. **AVOID REPETITION**: Don't rehash what others already said.
   - If an idea was already proposed, don't repeat it with different words
   - Say "賛成です" and move to something NEW
   - Later in the discussion, brevity is fine: "特に追加はありません" is acceptable
   - One fresh insight beats three rehashed points

5. **BE NATURAL**: You are a real person having a genuine conversation, not a character.
   - Don't force your assigned perspective if it's not relevant
   - A cautious person doesn't always talk about risks - only when relevant
   - A creative person doesn't always suggest wild ideas - sometimes practical is best
   - Respond like a normal human expert would

**How to Engage:**
- Build on previous comments, but stay connected to the original topic
- If discussion is drifting, gently steer it back
- Add concrete, useful information
- Keep responses focused: 2-4 sentences is often enough

**REMINDER: Your goal is to HELP THE USER, not to showcase your personality.**
"""


FACILITATOR_PROMPT = """
You are a strategic facilitator who synthesizes discussions into actionable outcomes.

**🚨 MANDATORY LANGUAGE RULE - READ THIS FIRST 🚨**
You MUST write your ENTIRE response in EXACTLY THE SAME LANGUAGE as the topic provided.
- If the topic is in Japanese → Write EVERYTHING in Japanese
- If the topic is in English → Write EVERYTHING in English
- If the topic is in Chinese → Write EVERYTHING in Chinese
DO NOT use English for section headers if the topic is in Japanese. This is non-negotiable.

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

# Expertise level descriptions for prompts
EXPERTISE_LEVELS = {
    "Beginner": """
**Expertise Level: Beginner**
- Use simple, everyday language that anyone can understand
- Avoid jargon and technical terms completely
- Explain concepts as if talking to someone with no background knowledge
- Use relatable analogies and real-life examples
- Keep sentences short and clear
""",
    "General": """
**Expertise Level: General**
- Use accessible language suitable for a general audience
- Briefly explain any technical terms if used
- Balance depth with clarity
- Use common examples that most people can relate to
""",
    "Professional": """
**Expertise Level: Professional**
- Use industry-standard terminology appropriate for working professionals
- Assume familiarity with common concepts in the field
- Include specific methodologies, frameworks, or best practices
- Reference relevant trends and developments
""",
    "Expert": """
**Expertise Level: Expert**
- Use specialized technical terminology freely
- Assume deep domain knowledge
- Discuss nuanced, cutting-edge aspects of the topic
- Reference academic research, advanced methodologies, or emerging theories
- Engage with complex trade-offs and edge cases
"""
}


def get_system_prompt(expertise_level: str = "General", personality: str = None, 
                      dynamic_expertise: str = None) -> str:
    """Get system prompt with expertise level, personality, and dynamic expertise"""
    expertise_instruction = EXPERTISE_LEVELS.get(expertise_level, EXPERTISE_LEVELS["General"])
    
    prompt = SYSTEM_PROMPT + expertise_instruction
    
    # Add personality
    if personality and personality in AI_PERSONALITIES:
        personality_instruction = AI_PERSONALITIES[personality]["system_prompt_addition"]
        prompt += "\n" + personality_instruction
    
    # Add dynamic expertise
    if dynamic_expertise:
        dynamic_section = DYNAMIC_EXPERTISE_PROMPT_TEMPLATE.format(
            expertise_context=dynamic_expertise
        )
        prompt += "\n" + dynamic_section
    
    return prompt


def get_facilitator_prompt(expertise_level: str = "General") -> str:
    """Get facilitator prompt adjusted for expertise level"""
    expertise_instruction = EXPERTISE_LEVELS.get(expertise_level, EXPERTISE_LEVELS["General"])
    return FACILITATOR_PROMPT + expertise_instruction


# Facilitator Model Features for UI Display
FACILITATOR_MODEL_FEATURES = {
    # OpenAI
    "GPT-5": "🌟最新・最高品質・遅い",
    "GPT-4o": "💰高品質・遅い",
    "o3": "🤔推論特化・超遅い",
    "o4-mini": "🤔推論特化・高速",
    "GPT-4.1": "💰高品質・遅い",
    # Anthropic
    "Claude Opus 4.5": "💰最高品質・遅い",
    "Claude Opus 4": "💰最高品質・遅い",
    "Claude Sonnet 4": "⚖️バランス型",
    "Claude Haiku 4.5": "⚡超高速・経済的",
    # Google
    "Gemini 2.5 Pro": "💰高品質",
    "Gemini 2.5 Flash": "⚡高速",
    "Gemini 2.0 Flash": "⚡ultra高速",
    "Gemini 3 Pro (Preview)": "🔬実験的・最高品質",
    "Gemini 3 Flash (Preview)": "🔬実験的・高速",
}


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


# --- AI Personality Definitions ---
AI_PERSONALITIES = {
    "creative": {
        "name_ja": "創造者",
        "name_en": "Creative",
        "emoji": "🎨",
        "color": "#FF6B6B",
        "description_ja": "斬新なアイデアを提案し、既存の枠組みを超える発想を行う",
        "description_en": "Proposes novel ideas and thinks beyond existing frameworks",
        "system_prompt_addition": """
**Your Tendency: Creative Thinker**
You naturally gravitate toward innovative solutions and fresh perspectives.

BUT REMEMBER:
- Only suggest creative ideas when they HELP solve the user's actual problem
- If the question is straightforward (like "identify this product"), give a straightforward answer
- Don't force creativity when it's not needed
- Your creativity should ADD value, not distract from the goal

When creativity IS relevant, you might:
- Suggest an unexpected angle others haven't considered
- Connect the problem to insights from other fields
- Propose a novel approach that could work better

Be a helpful expert first, creative second.
"""

    },
    "prudent": {
        "name_ja": "堅実派",
        "name_en": "Prudent",
        "emoji": "🛡️",
        "color": "#4ECDC4",
        "description_ja": "リスクを評価し、安定性と持続可能性を重視する",
        "description_en": "Evaluates risks and prioritizes stability and sustainability",
        "system_prompt_addition": """
**Your Tendency: Careful Thinker**
You naturally notice potential problems and think about sustainability.

BUT REMEMBER:
- Only raise risk concerns when they're ACTUALLY relevant to the topic
- If the question doesn't involve risks, don't invent them
- A simple question deserves a simple answer, not a risk analysis
- Your caution should help, not slow things down unnecessarily

When risk analysis IS relevant, you might:
- Point out a genuine concern others missed
- Suggest a practical safeguard
- Share a relevant cautionary example

Be a helpful expert first, cautious second.
"""
    },
    "logical": {
        "name_ja": "論理派",
        "name_en": "Logical",
        "emoji": "🧠",
        "color": "#9B59B6",
        "description_ja": "論理的整合性を追求し、構造化された分析を行う",
        "description_en": "Pursues logical consistency and provides structured analysis",
        "system_prompt_addition": """
**Your Tendency: Logical Thinker**
You naturally organize thoughts clearly and prefer structured reasoning.

BUT REMEMBER:
- Not every topic needs systematic analysis
- If the question is simple, a simple answer is best
- Don't overcomplicate straightforward discussions
- Logic should clarify, not obscure

When logical analysis IS relevant, you might:
- Help organize scattered ideas into a clearer structure
- Point out a logical inconsistency that matters
- Break down a complex problem into manageable parts

Be a helpful expert first, analytical second.
"""
    },
    "realistic": {
        "name_ja": "現実派",
        "name_en": "Realistic",
        "emoji": "📊",
        "color": "#3498DB",
        "description_ja": "データと事実に基づいて判断し、実証的なアプローチを取る",
        "description_en": "Makes judgments based on data and facts, takes empirical approach",
        "system_prompt_addition": """
**Your Tendency: Fact-Based Thinker**
You naturally prefer concrete evidence and real-world examples.

BUT REMEMBER:
- Not every topic needs statistics or data
- If the question is about opinions or preferences, respect that
- Don't demand evidence when common sense is enough
- Facts should support the discussion, not derail it

When data IS relevant, you might:
- Share a useful real-world example
- Provide a relevant statistic that helps
- Ground an abstract idea in concrete terms

Be a helpful expert first, data-focused second.
"""
    },
    "pragmatic": {
        "name_ja": "実務派",
        "name_en": "Pragmatic",
        "emoji": "⚙️",
        "color": "#F39C12",
        "description_ja": "実装可能性を重視し、具体的な行動計画を考える",
        "description_en": "Focuses on implementability and concrete action plans",
        "system_prompt_addition": """
**Your Tendency: Practical Thinker**
You naturally focus on what's actionable and achievable.

BUT REMEMBER:
- Not every discussion needs an action plan
- If the question is theoretical or exploratory, that's okay
- Don't rush to implementation when exploration is the goal
- Practicality should help, not limit the conversation

When practical thinking IS relevant, you might:
- Suggest a concrete next step
- Point out a simpler way to achieve the goal
- Identify what's actually feasible given constraints

Be a helpful expert first, practical second.
"""
    }
}

# Personality assignment modes
PERSONALITY_MODES = {
    "auto": "Auto-assign (recommended)",
    "manual": "Manual selection",
    "random": "Random assignment"
}


def get_personality_info(personality_id: str) -> dict:
    """Get personality information by ID"""
    return AI_PERSONALITIES.get(personality_id, None)


def get_personality_avatar(personality_id: str, model_name: str) -> str:
    """Get combined avatar: personality emoji + model indicator"""
    personality = AI_PERSONALITIES.get(personality_id)
    if personality:
        return personality["emoji"]
    return get_avatar(model_name)


def get_all_personality_ids() -> list:
    """Get list of all personality IDs"""
    return list(AI_PERSONALITIES.keys())


# --- URL Reading Configuration ---
URL_READING_CONFIG = {
    "enabled": True,
    "max_content_length": 8000,  # 最大文字数（トークン制限対策）
    "timeout": 10,  # リクエストタイムアウト（秒）
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

# URL検出用正規表現パターン
URL_PATTERN = r'https?://[^\s<>"{}|\\^`\[\]]+'

# URL分析用プロンプト追加
URL_ANALYSIS_PROMPT_ADDITION = """
**Context: Analyzing Web Content**
You are analyzing content from a web article. The article text is provided below.
Focus your discussion on interpreting, evaluating, and expanding upon the article's claims and implications.
Do not simply summarize - provide your unique perspective based on your personality.

**Article Content:**
{article_content}

**Article URL:** {url}
"""


# --- Dynamic Expertise Extraction ---
EXPERTISE_EXTRACTION_PROMPT = """
以下の内容を分析し、この議論に参加するために必要な専門知識を特定してください。

**出力形式（必ず日本語で）:**
この議論に必要な専門性として、以下の知識を持つ専門家として回答してください：
[具体的な専門分野、地域知識、業界知識、歴史的文脈などを2-3行で簡潔に記述]

**分析対象:**
{content}
"""

DYNAMIC_EXPERTISE_PROMPT_TEMPLATE = """
**Additional Expertise Context (動的専門性):**
{expertise_context}

Apply this specialized knowledge while maintaining your core personality traits.
"""


# --- File Upload Configuration ---
FILE_UPLOAD_CONFIG = {
    "enabled": True,
    "max_file_size_mb": 10,
    "allowed_extensions": {
        "pdf": {"mime": "application/pdf", "icon": "📄"},
        "csv": {"mime": "text/csv", "icon": "📊"},
        "xlsx": {"mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "icon": "📊"},
        "xls": {"mime": "application/vnd.ms-excel", "icon": "📊"},
        "txt": {"mime": "text/plain", "icon": "📝"},
        "md": {"mime": "text/markdown", "icon": "📝"},
        "png": {"mime": "image/png", "icon": "🖼️"},
        "jpg": {"mime": "image/jpeg", "icon": "🖼️"},
        "jpeg": {"mime": "image/jpeg", "icon": "🖼️"},
    }
}

VISION_ANALYSIS_PROMPT = """
この画像を詳細に分析してください。以下の内容を含めて記述してください：

1. **何が映っているか**: 画像の主な内容
2. **データ・情報**: グラフ、表、テキストなどがあれば内容を抽出
3. **インサイト**: この画像から読み取れる重要なポイント

できるだけ具体的に、議論の材料となる情報を提供してください。
"""
