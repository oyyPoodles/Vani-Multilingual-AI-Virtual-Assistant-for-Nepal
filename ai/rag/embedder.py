"""
VANI — Document Embedder
Embeds text chunks using pretrained sentence-transformers.
"""

import logging
import numpy as np
from typing import List, Dict

logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════
# TRAINING PLACEHOLDER
# This section is intentionally left for
# execution on a separate training machine.
# Dataset: datasets/knowledge_base/
# Model: sentence-transformers/all-MiniLM-L6-v2
# Output: ai/rag/models/embedder_finetuned/
# ═══════════════════════════════════════════


class DocumentEmbedder:
    """Embeds document chunks using sentence-transformers (pretrained)."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None

    def load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded: {self.model_name}")
        except ImportError:
            raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")

    def embed_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Embed a list of text strings."""
        if self.model is None:
            self.load_model()
        embeddings = self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)
        logger.info(f"Embedded {len(texts)} texts -> shape {embeddings.shape}")
        return embeddings

    def embed_chunks(self, chunks: List[Dict], batch_size: int = 32) -> List[Dict]:
        """Embed document chunks and attach embeddings."""
        if self.model is None:
            self.load_model()

        texts = [c["text"] for c in chunks]
        embeddings = self.embed_texts(texts, batch_size=batch_size)

        for i, chunk in enumerate(chunks):
            chunk["embedding"] = embeddings[i].tolist()

        return chunks
