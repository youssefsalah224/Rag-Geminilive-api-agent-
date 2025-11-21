# LiveKit Voice Agent with Gemini Live API and RAG

A real-time voice AI agent that combines LiveKit's audio streaming infrastructure with Google's Gemini Live API and Retrieval-Augmented Generation (RAG) for context-aware conversations.

## Features

- **Real-time Voice Interaction** - Natural conversations with low-latency audio streaming
- **Gemini Live API** - End-to-end voice processing (speech input + audio output)
- **RAG-Enhanced Responses** - Retrieves relevant context from knowledge base before answering
- **Live Transcripts** - Real-time text display of conversations with auto-scroll
- **Visual State Feedback** - Pulsing animations show agent status (listening, processing, speaking)
- **Retrieved Context Display** - See what information the AI is using to answer questions
- **Material Design 3 UI** - Clean, modern interface optimized for voice interactions

## Architecture

### Frontend (React + vite )

- **LiveKit Client SDK** - WebRTC audio streaming
- **React Components** - Voice control center, live transcripts, context panels
- **Vite** - Responsive, accessible design
- **Custom Animations** - Pulsing rings for voice states

### Backend (Node.js )

- **Token Generation** - Secure access token creation and matching it to the front
- **Session Management** - Track conversations and context
- **API Endpoints** - Token generation, health checks, session data

### Python Agent Service

- **LiveKit Agents Framework** - Voice agent lifecycle management
- **Gemini Live API Integration** - `gemini-2.0-flash-exp` model
- **RAG System** - FAISS vector store + Sentence Transformers(from hugging face)
- **Knowledge Base** - documents about LiveKit, Gemini, and RAG

## 🚀 Quick Start

### Prerequisites

- **Node.js 20+** (for frontend and backend)
- **Python 3.11+** (for voice agent)
- **LiveKit Account** - Get credentials at https://cloud.livekit.io/
- **Google AI API Key** - Get from https://aistudio.google.com/app/apikey

### 1. Environment Setup

Secrets you should have :

- `LIVEKIT_API_KEY`
- `LIVEKIT_API_SECRET`
- `LIVEKIT_URL`
- `GOOGLE_API_KEY`

### 2. Install Dependencies

#### Frontend & Backend (Node.js)

```bash
npm install
```

#### Python Agent

```bash
cd python_agent
pip install -r requirements.txt
```

### 3. Start the Services

#### Terminal 1: Frontend & Backend

```bash
npm run dev
```

```bash
python server.py runserver
```

This starts both:

- Express backend on port 5000 (serves frontend + API)
- Vite dev server for hot module replacement

#### Terminal 2: Python Voice Agent

**Important**: The Python agent integrated with the room token genration feature so its already know which room to join .

```bash
python  agent.py dev
```

The agent will:

- Initialize the RAG system (build FAISS index)
- Connect to LiveKit
- Join the specified room automatically

## 📁 Project Structure

```
.
├── frontend/                 # React frontend
│   ├── src/                 # Source code for the frontend
│   │   ├── components/      # Reusable React components (e.g., LiveKitModal, SimpleVoiceAssistant)
│   │   ├── assets/          # Static assets (images, icons, etc.)
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Global styles
│   │   ├── main.jsx         # Entry point for React app
│   │   └── index.css        # Additional styles
│   ├── public/              # Public static files
│   ├── package.json         # Frontend dependencies and scripts
│   ├── vite.config.js       # Vite configuration
│   └── README.md            # Frontend documentation
│
├── backend/                 # Python backend
│   ├── agent.py             # Main voice agent logic
│   ├── server.py            # Backend server for API and token generation
│   ├── knowledgephase.py    # Knowledge base management
│   ├── rag.py               # Retrieval-Augmented Generation system
│   ├── requirements.txt     # Python dependencies
│   ├── sample.env           # Environment variable template
│   └── README.md            # Backend documentation
│
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
└── LICENSE                  # Project license
```

## 🧠 RAG System

### Knowledge Base Topics

- LiveKit Voice Agents overview
- Gemini Live API integration
- RAG system features
- Voice agent states
- LiveKit room management
- Audio streaming pipeline
- Transcript management
- Context injection
- Getting started guide
- Best practices

### How It Works

1. User speaks a question
2. Speech transcribed by Gemini Live API
3. RAG system embeds the question using Sentence Transformers
4. FAISS retrieves top-3 most similar documents (cosine similarity)
5. Context injected into Gemini's prompt
6. AI generates answer using both its knowledge + retrieved context
7. Response streamed back as audio

### RAG Performance

- **Embedding Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Retrieval Time**: ~10-50ms for top-3 documents
- **Index**: FAISS Inner Product (normalized for cosine similarity)

## Configuration

### Gemini Voice Options

Edit `python_agent/agent.py` to change voice:

```python
voice="Puck"
```

### Agent Instructions

Customize behavior in `VoiceAssistantAgent.__init__()`:

```python
instructions = """Your custom instructions here..."""
```

## 📊 Monitoring & Logs

### Backend Logs

- Check terminal running `npm run dev`
- API requests logged with timestamps

### Python Agent Logs

- Terminal running `python agent.py dev`
- Shows RAG retrievals, agent state changes
- Gemini Live API interactions

## 🚢 Deployment

### Backend

The Node.js application is ready for Replit deployment:

```bash
python server.py runserver
```

### Backend

```bash
npm run dev
```

### Python Agent

Deploy separately or run as a background service:

```bash
python agent.py dev
```

## Resources

- **LiveKit Docs**: https://docs.livekit.io/
- **Gemini Live API**: https://ai.google.dev/gemini-api/docs/live
- **LiveKit Agents**: https://docs.livekit.io/agents/
- **FAISS**: https://github.com/facebookresearch/faiss
- **Sentence Transformers**: https://www.sbert.net/

