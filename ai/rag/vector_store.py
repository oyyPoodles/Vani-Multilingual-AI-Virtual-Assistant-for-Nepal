"""
VANI — Vector Store
Manages ChromaDB / Qdrant vector storage for RAG retrieval.
"""

import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

PERSIST_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'vectordb')


class VectorStore:
    """Manages vector storage using ChromaDB."""

    def __init__(self, collection_name: str = "vani_knowledge", persist_dir: str = None):
        self.collection_name = collection_name
        self.persist_dir = persist_dir or PERSIST_DIR
        self.client = None
        self.collection = None

    def initialize(self):
        """Initialize ChromaDB client and collection."""
        try:
            import chromadb
            from chromadb.config import Settings

            os.makedirs(self.persist_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persist_dir)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"VectorStore initialized: collection='{self.collection_name}', "
                        f"count={self.collection.count()}")
        except ImportError:
            raise ImportError("chromadb not installed. Run: pip install chromadb")

    def add_documents(self, chunks: List[Dict]):
        """Add document chunks to the vector store."""
        if self.collection is None:
            self.initialize()

        ids = [f"doc_{c.get('metadata', {}).get('source', 'unknown')}_{c['chunk_id']}" for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [c.get("metadata", {}) for c in chunks]

        # Add embeddings if available, otherwise let ChromaDB compute them
        if "embedding" in chunks[0]:
            embeddings = [c["embedding"] for c in chunks]
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)
        else:
            self.collection.add(ids=ids, documents=documents, metadatas=metadatas)

        logger.info(f"Added {len(chunks)} chunks to vector store. Total: {self.collection.count()}")

    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """Query the vector store for similar documents."""
        if self.collection is None:
            self.initialize()

        results = self.collection.query(query_texts=[query_text], n_results=top_k)

        documents = []
        for i in range(len(results['ids'][0])):
            documents.append({
                "id": results['ids'][0][i],
                "text": results['documents'][0][i],
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                "distance": results['distances'][0][i] if results['distances'] else None
            })

        return documents

    def delete_collection(self):
        """Delete the entire collection."""
        if self.client:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")

    def get_count(self) -> int:
        if self.collection is None:
            self.initialize()
        return self.collection.count()
