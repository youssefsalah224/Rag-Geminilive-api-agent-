import os
import json
import asyncio
from dotenv import load_dotenv
from livekit import agents, rtc
from livekit.agents import AgentSession, Agent
from livekit.plugins import google

from rag import get_rag_system

# Load environment variables
load_dotenv()


class VoiceAssistantAgent(Agent):

    def __init__(self, rag_system, room: rtc.Room):
        self.rag_system = rag_system
        self.conversation_history = []
        self.room = room

        instructions = """You are a helpful AI voice assistant your default language is English you are powered by LiveKit and Gemini Live API.
You have access to a knowledge base about LiveKit Voice Agents, Gemini Live API, and RAG systems.
When answering questions, use the provided context from the knowledge base to give accurate,
informative responses.
Be conversational, friendly, and concise. Speak naturally as if you're having a voice conversation.
If you don't have enough context to answer a question accurately, say so honestly.
Remember you're in a voice conversation, so keep responses clear and well-paced for speech."""
        
        super().__init__(instructions=instructions)
    
    async def send_data_message(self, message_type: str, data: dict):
        payload = {
            "type": message_type,
            **data
        }
        message_bytes = json.dumps(payload).encode('utf-8')
        await self.room.local_participant.publish_data(
            message_bytes,
            reliable=True
        )
    
    async def on_user_speech(self, text: str):
        """
        Called when user speech is transcribed
        Retrieve RAG context and inject it into the conversation
        """
        print(f"\n[User Speech] {text}")
        
        # Send user transcript to frontend
        await self.send_data_message("transcript", {
            "id": f"user_{len(self.conversation_history)}",
            "role": "user",
            "content": text,
            "timestamp": int(asyncio.get_event_loop().time() * 1000)
        })
        
        await self.send_data_message("agent_state", {
            "state": "processing"
        })
        
        retrieved_docs = self.rag_system.retrieve(text, top_k=3)
        if retrieved_docs:
            print(f" Retrieved {len(retrieved_docs)} relevant documents")
            for doc in retrieved_docs:
                print(f"  - {doc['source']} (score: {doc['relevanceScore']:.3f})")
            
            formatted_contexts = [{
                "id": doc["id"],
                "source": doc["source"],
                "snippet": doc["content"],
                "relevanceScore": doc["relevanceScore"]
            } for doc in retrieved_docs]
            await self.send_data_message("rag_context", {
                "contexts": formatted_contexts
            })
            
            context = self.rag_system.format_context_for_prompt(retrieved_docs)
            
            self.conversation_history.append({
                "role": "user",
                "text": text,
                "context": context,
                "retrieved_docs": retrieved_docs
            })
        else:
            print("No relevant context found")
            await self.send_data_message("rag_context", {
                "contexts": []
            })
            self.conversation_history.append({
                "role": "user",
                "text": text,
                "context": None,
                "retrieved_docs": []
            })
    
    async def on_agent_speech(self, text: str):
        """Called when agent generates a response"""
        print(f"\n[Agent Speech] {text}")
        
        # Update agent state to speaking
        await self.send_data_message("agent_state", {
            "state": "speaking"
        })
        
        # Send agent transcript to frontend
        await self.send_data_message("transcript", {
            "id": f"agent_{len(self.conversation_history)}",
            "role": "agent",
            "content": text,
            "timestamp": int(asyncio.get_event_loop().time() * 1000)
        })
        await asyncio.sleep(0.5)  # Brief delay for natural transition
        await self.send_data_message("agent_state", {
            "state": "idle"
        })


async def entrypoint(ctx: agents.JobContext):
    print(f"Starting Voice Agent for room: {ctx.room.name}")
    rag_system = get_rag_system()

    voice_agent = VoiceAssistantAgent(rag_system, ctx.room)
    try:
        print(f"[Gemini] Model initialized: gemini-2.0-flash-exp with voice 'Puck'")
        session = AgentSession(
            llm= google.beta.realtime.RealtimeModel(
            model="gemini-2.0-flash-exp",
            voice="Puck",  
            temperature=0.8,
            instructions=voice_agent.instructions,
            modalities=["AUDIO"], 
        ),
        )
        
        print(f"[LiveKit] Agent session created")
        print(f"[LiveKit] Joining room: {ctx.room.name}")
        
        # Start the agent session in the LiveKit room
        await session.start(
            room=ctx.room,
            agent=voice_agent
        )
        
        print(f"[Success] Voice agent is now active and listening!")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize agent: {e}")
        raise


def main():
    """Run the LiveKit agent worker"""
    print(f" LiveKit URL: {os.getenv('LIVEKIT_URL')}")
    print("\n Starting LiveKit Agent Worker...\n")
    
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
        )
    )


if __name__ == "__main__":
    main()

