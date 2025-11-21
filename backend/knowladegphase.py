"""
knowladge base 
Contains sample FAQs  about LiveKit Voice Agents
"""

KNOWLEDGE_BASE = [
    {
        "id": "kb_001",
        "source": "LiveKit Voice Agents Overview",
        "content": """LiveKit Agents is a framework for building real-time voice AI agents. 
        It provides a high-level API for creating voice-enabled applications that can listen to users, 
        process speech in real-time, and respond with natural-sounding voices. The framework handles 
        audio streaming, participant management, and room connections automatically."""
    },
    {
        "id": "kb_002",
        "source": "Gemini Live API Integration",
        "content": """The Gemini Live API from Google provides end-to-end voice processing capabilities. 
        Unlike traditional STT → LLM → TTS pipelines, Gemini Live handles both speech input and audio 
        output natively in a streaming fashion. It supports models like gemini-2.0-flash-exp with 
        multiple voice options including Puck, Charon, Kore, Fenrir, and Aoede."""
    },
    {
        "id": "kb_003",
        "source": "RAG System Features",
        "content": """Retrieval-Augmented Generation (RAG) enhances AI responses by retrieving relevant 
        information from a knowledge base before generating answers. The system uses vector embeddings 
        to find semantically similar content, then passes this context to the AI model. This ensures 
        responses are grounded in accurate, up-to-date information rather than relying solely on 
        the model's training data."""
    },
    {
        "id": "kb_004",
        "source": "Voice Agent States",
        "content": """A voice agent can be in different states: idle (ready to listen), listening 
        (actively capturing user speech), processing (analyzing input and retrieving context), 
        and speaking (delivering the AI response). Visual feedback through pulsing animations 
        helps users understand the current state: blue for listening, amber for processing, 
        and green for speaking."""
    },
    {
        "id": "kb_005",
        "source": "LiveKit Room Management",
        "content": """LiveKit rooms are virtual spaces where participants can communicate in real-time. 
        Each room has a unique name and participants join using access tokens. The token system 
        provides security by encoding permissions (like the ability to publish audio, subscribe to 
        streams, or send data messages) and has a configurable time-to-live (TTL) for expiration."""
    },
    {
        "id": "kb_006",
        "source": "Audio Streaming Pipeline",
        "content": """The audio streaming pipeline connects user microphone input through the LiveKit 
        room to the Gemini Live API for processing. Audio is captured in real-time, sent to the 
        cloud for analysis, and responses are streamed back as audio. This bi-directional streaming 
        enables natural, low-latency conversations without waiting for complete sentences."""
    },
    {
        "id": "kb_007",
        "source": "Transcript Management",
        "content": """Live transcripts provide a text record of the conversation between users and 
        the AI agent. Transcripts include timestamps, speaker identification (user vs agent), and 
        the actual spoken content. They support features like auto-scroll to the latest message, 
        manual scroll with a jump-to-bottom button, and responsive message bubbles that adapt to 
        different screen sizes."""
    },
    {
        "id": "kb_008",
        "source": "Context Injection",
        "content": """Before the AI agent responds, retrieved context from the knowledge base is 
        injected into the prompt. This context includes the most relevant snippets based on 
        semantic similarity to the user's question, along with relevance scores. The agent can 
        then reference this information to provide accurate, contextual answers."""
    },
    {
        "id": "kb_009",
        "source": "Getting Started",
        "content": """To use the LiveKit Voice Agent, you need credentials: a LiveKit API key and 
        secret from cloud.livekit.io, a LiveKit server URL (typically wss://yourproject.livekit.cloud), 
        and a Google AI API key from aistudio.google.com. Once configured, simply click the 
        microphone button to start speaking, and the agent will listen, process your question using 
        RAG for context, and respond with a natural voice."""
    },
    {
        "id": "kb_010",
        "source": "Best Practices",
        "content": """For optimal voice agent performance: speak clearly and at a normal pace, 
        wait for the processing indicator before speaking again, use headphones to prevent echo, 
        ensure a stable internet connection for low-latency streaming, and review the retrieved 
        context panel to understand what information the AI is using to formulate its responses."""
    },
]


def get_all_documents():
    """Return all knowledge base documents"""
    return KNOWLEDGE_BASE
def get_document_by_id(doc_id: str):
    """Retrieve a specific document by ID"""
    for doc in KNOWLEDGE_BASE:
        if doc["id"] == doc_id:
            return doc
    return None


def get_documents_count():
    """Return the total number of documents in the knowledge base"""
    return len(KNOWLEDGE_BASE)