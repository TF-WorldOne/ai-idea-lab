# X-Think AI Idea Lab

**Premium Multi-AI Collaborative Brainstorming Platform**

[![Live Demo](https://img.shields.io/badge/Live-Demo-gold?style=for-the-badge)](https://x-think.xworld.one/)
[![Cloud Run](https://img.shields.io/badge/Google-Cloud%20Run-4285F4?style=for-the-badge&logo=google-cloud)](https://cloud.google.com/run)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

## 🌟 Overview

X-Think AI Idea Lab is a sophisticated brainstorming platform that orchestrates multiple AI personalities to generate, critique, and synthesize ideas collaboratively. Built with a premium Gold & Black aesthetic, it provides an immersive environment for creative thinking and problem-solving.

**Live Application**: [https://x-think.xworld.one/](https://x-think.xworld.one/)

## ✨ Key Features

### 🤖 Multi-AI Collaboration
- **6 Distinct AI Personalities**: Each with unique thinking styles and expertise
  - **Innovator**: Creative, unconventional ideas
  - **Analyst**: Data-driven, logical analysis
  - **Critic**: Constructive criticism and risk assessment
  - **Synthesizer**: Integration and pattern recognition
  - **Pragmatist**: Practical implementation focus
  - **Visionary**: Long-term strategic thinking

### 💬 Interactive Discussion Canvas
- **Three-Column Layout**: Simultaneous view of all AI contributions
- **Real-time Streaming**: Watch AI responses generate in real-time
- **Turn-based Discussion**: Structured conversation flow with configurable turn limits
- **Context Awareness**: AIs reference and build upon previous contributions

### 🎯 Intelligent Facilitation
- **AI Facilitator**: Automatically synthesizes discussion into actionable insights
- **Multiple Report Formats**:
  - Executive Summary
  - Action Plan
  - Pros & Cons Analysis
  - SWOT Analysis
  - Risk Assessment
  - Innovation Roadmap
- **Model Selection**: Choose from GPT-4, Claude, or Gemini for facilitation

### 📤 Export & Integration
- **Multiple Export Formats**:
  - Markdown (.md)
  - Text (.txt)
  - JSON (.json)
  - PDF (.pdf)
- **NotebookLM Integration**: Direct export to Google NotebookLM Enterprise
- **Downloadable Reports**: Save discussions and synthesis reports locally

### 🎨 Premium UI/UX
- **Gold & Black Theme**: Sophisticated, professional aesthetic
- **Responsive Design**: Optimized for desktop and tablet
- **Smooth Animations**: Polished micro-interactions
- **Accessibility**: High contrast, readable typography

### 🔧 Advanced Configuration
- **Custom AI Personalities**: Create and save custom AI personas
- **Priming Content**: Upload documents or paste text to prime discussions
- **Model Selection**: Choose AI models per personality
- **Turn Control**: Configure discussion length (5-20 turns)

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **AI Models**: 
  - OpenAI GPT-4
  - Anthropic Claude 3.5
  - Google Gemini 2.0 Flash
- **Deployment**: Google Cloud Run
- **Container Registry**: Google Artifact Registry
- **Hosting**: Firebase Hosting (custom domain)
- **Authentication**: Firebase Auth (Google Sign-In)

### Project Structure
```
ai-idea-lab/
├── app.py                          # Main Streamlit application
├── ai_config.py                    # AI personality configurations
├── notebooklm_integration.py       # NotebookLM export functionality
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Container configuration
├── deploy.bat                      # Deployment script
├── firebase.json                   # Firebase Hosting config
├── .firebaserc                     # Firebase project config
├── assets/
│   ├── logo.png                    # Application logo
│   └── siteicon.png                # Favicon
└── public/                         # Firebase Hosting public directory
```

## 🚀 Deployment

### Prerequisites
- Google Cloud Platform account
- Firebase project
- Docker Desktop (for local testing)
- Google Cloud SDK (`gcloud` CLI)

### Environment Variables
Set the following secrets in Google Cloud Secret Manager:
- `OPENAI_API_KEY`: OpenAI API key
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GOOGLE_API_KEY`: Google AI API key

### Deploy to Cloud Run
```bash
# Run deployment script
.\deploy.bat
```

The script will:
1. Build Docker image
2. Push to Artifact Registry
3. Deploy to Cloud Run
4. Configure service settings

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py --server.port=8080
```

## 📋 Configuration

### AI Personalities
Edit `ai_config.py` to customize AI personalities:
```python
PERSONALITIES = {
    "personality_name": {
        "name": "Display Name",
        "emoji": "🎯",
        "description": "Personality description",
        "system_prompt": "System prompt for AI",
        "default_model": "gpt-4"
    }
}
```

### Firebase Hosting
Configure custom domain in `firebase.json`:
```json
{
    "hosting": {
        "public": "public",
        "rewrites": [{
            "source": "**",
            "run": {
                "serviceId": "ai-idea-lab",
                "region": "asia-northeast1"
            }
        }]
    }
}
```

## 🔐 Authentication

The application uses Firebase Authentication with Google Sign-In provider. Authentication is currently **optional** (removed mandatory login gate for frictionless access).

To re-enable authentication:
1. Uncomment authentication check in `app.py`
2. Configure Firebase Auth in GCP Console
3. Redeploy application

## 📊 Usage

### Starting a Discussion
1. **Enter Topic**: Describe your brainstorming topic or question
2. **Select Participants**: Choose 3-6 AI personalities
3. **Configure Settings**:
   - Number of turns (5-20)
   - AI models for each personality
   - Optional: Upload priming documents
4. **Start Discussion**: Click "🚀 ディスカッション開始"

### During Discussion
- Watch real-time AI responses in three columns
- Observe turn-by-turn progression
- Wait for completion or stop early

### After Discussion
1. **Generate Report**: Click "📊 レポート生成"
2. **Select Format**: Choose report type
3. **Choose Facilitator**: Select AI model
4. **Export**: Download in preferred format or send to NotebookLM

## 🛠️ Troubleshooting

### Common Issues

**Build fails with "out of space" error**
- Solution: Use Artifact Registry instead of Container Registry (already configured)

**Authentication errors**
- Check Firebase configuration in GCP Console
- Verify API keys in Secret Manager

**AI responses not streaming**
- Check API keys are correctly set
- Verify model availability in your region

## 📝 License

This project is proprietary software. All rights reserved.

## 🤝 Contributing

This is a private project. For questions or issues, contact the development team.

## 📞 Support

For support, please contact: [Your Contact Information]

---

**Built with ❤️ using Streamlit, Google Cloud, and cutting-edge AI models**
