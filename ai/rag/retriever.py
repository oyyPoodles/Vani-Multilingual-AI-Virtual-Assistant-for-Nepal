"""
VANI — RAG Retriever
Top-K semantic retrieval with context assembly for LLM prompting.
"""

import logging
from typing import List, Dict, Optional
from .vector_store import VectorStore
from .chunker import DocumentChunker
from .embedder import DocumentEmbedder

logger = logging.getLogger(__name__)


class RAGRetriever:
    """Full RAG pipeline: chunk → embed → store → retrieve → context."""

    def __init__(self, collection_name: str = "vani_knowledge"):
        self.vector_store = VectorStore(collection_name=collection_name)
        self.chunker = DocumentChunker()
        self.embedder = DocumentEmbedder()

    def ingest_file(self, filepath: str):
        """Ingest a single document file into the vector store."""
        chunks = self.chunker.chunk_file(filepath)
        chunks = self.embedder.embed_chunks(chunks)
        self.vector_store.add_documents(chunks)
        logger.info(f"Ingested {filepath}: {len(chunks)} chunks")

    def ingest_directory(self, dir_path: str):
        """Ingest all documents from a directory."""
        chunks = self.chunker.chunk_directory(dir_path)
        if chunks:
            chunks = self.embedder.embed_chunks(chunks)
            self.vector_store.add_documents(chunks)
        logger.info(f"Ingested directory {dir_path}: {len(chunks)} total chunks")

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve top-K relevant documents for a query."""
        return self.vector_store.query(query, top_k=top_k)

    def build_context(self, query: str, top_k: int = 5) -> str:
        """
        Build LLM context from retrieved documents.

        Returns:
            Formatted context string for LLM prompting
        """
        docs = self.retrieve(query, top_k=top_k)

        if not docs:
            return "No relevant context found."

        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.get("metadata", {}).get("source", "unknown")
            context_parts.append(f"[Source {i}: {source}]\n{doc['text']}")

        return "\n\n---\n\n".join(context_parts)

    def generate_prompt(self, query: str, language: str = "en", top_k: int = 5) -> str:
        """
        Generate a full RAG prompt for LLM.

        Args:
            query: User query
            language: Response language ('ne' or 'en')
            top_k: Number of context documents

        Returns:
            Complete prompt string
        """
        context = self.build_context(query, top_k=top_k)

        lang_instruction = {
            "ne": "Respond in Nepali (Devanagari script).",
            "en": "Respond in English.",
            "mixed": "Respond in the same language mix as the user's query."
        }.get(language, "Respond in English.")

        prompt = f"""You are VANI, a helpful AI assistant for Nepal. Answer the user's question based on the provided context.
If the context doesn't contain relevant information, say so honestly.
{lang_instruction}

Context:
{context}

User Question: {query}

VANI Response:"""

        return prompt
