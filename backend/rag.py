import os
import json
import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import faiss
from knowladegphase import get_all_documents


class RAGSystem:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize RAG system with sentence transformer and FAISS index
        
        Args:
            model_name: HuggingFace model for embeddings (default: all-MiniLM-L6-v2)
        """
        print(f"Initializing RAG system with model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.documents = get_all_documents()
        self.index = None
        self.embeddings = None
        
        # Build index
        self._build_index()
        print(f"RAG system initialized with {len(self.documents)} documents")
    
    def _build_index(self):
        """Build FAISS index from knowledge base documents"""
        print("Building FAISS index...")

        texts = [doc["content"] for doc in self.documents]
        self.embeddings = self.model.encode(texts, convert_to_numpy=True)

        faiss.normalize_L2(self.embeddings)

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension) 
        self.index.add(self.embeddings)
        
        print(f"FAISS index built with {self.index.ntotal} vectors, dimension: {dimension}")
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve top-k most relevant documents for a query
        Args:
            query: User query text
            top_k: Number of documents to retrieve
        Returns:
            List of dictionaries with id, snippet, source, and relevance_score
        """
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append({
                    "id": doc["id"],
                    "snippet": doc["content"],
                    "source": doc["source"],
                    "relevanceScore": float(score)
                })
        
        return results
    
    def format_context_for_prompt(self, retrieved_docs: List[Dict]) -> str:
        """
        Format retrieved documents into a context string for the LLM
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        if not retrieved_docs:
            return ""
        
        context_parts = ["Here is relevant context to help answer the user's question:\n"]
        
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(f"\n[Context {i} - {doc['source']}]")
            context_parts.append(doc['snippet'])
        
        context_parts.append("\n\nPlease use this context when formulating your response.")
        
        return "\n".join(context_parts)

_rag_instance = None
def get_rag_system() -> RAGSystem:
    """Get or create RAG system singleton"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGSystem()
    return _rag_instance


if __name__ == "__main__":
    rag = RAGSystem()
    
    test_queries = [
        "How does the Gemini Live API work?",
        "What are the different voice agent states?",
        "How do I get started with LiveKit?"
    ]
    
    print("\n" + "=")
    print("Testing RAG System")

    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" )
        
        results = rag.retrieve(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['source']} (Score: {result['relevanceScore']:.3f})")
            print(f"   {result['snippet'][:150]}...")
        
        print("\nFormatted Context:")
        print(rag.format_context_for_prompt(results))
