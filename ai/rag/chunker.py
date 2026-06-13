"""
VANI — Document Chunker
Splits documents into overlapping chunks for RAG embedding.
"""

import os
import re
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 512   # tokens (approx chars / 4)
DEFAULT_OVERLAP = 50       # token overlap between chunks


class DocumentChunker:
    """Chunks documents for vector embedding."""

    def __init__(self, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP):
        self.chunk_size = chunk_size
        self.overlap = overlap
        # Approximate: 1 token ≈ 4 chars for English, ~2 chars for Nepali
        self.char_chunk_size = chunk_size * 3
        self.char_overlap = overlap * 3

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """
        Split text into overlapping chunks.

        Returns:
            List of dicts with keys: text, chunk_id, metadata
        """
        if not text.strip():
            return []

        # Split by paragraphs first, then merge/split to target size
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        current_chunk = ""
        chunk_id = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) < self.char_chunk_size:
                current_chunk += ("\n\n" + para if current_chunk else para)
            else:
                if current_chunk:
                    chunks.append(self._make_chunk(current_chunk, chunk_id, metadata))
                    chunk_id += 1
                    # Keep overlap
                    overlap_text = current_chunk[-self.char_overlap:] if len(current_chunk) > self.char_overlap else ""
                    current_chunk = overlap_text + "\n\n" + para
                else:
                    # Single paragraph larger than chunk size — force split
                    for sub_chunk in self._force_split(para):
                        chunks.append(self._make_chunk(sub_chunk, chunk_id, metadata))
                        chunk_id += 1
                    current_chunk = ""

        if current_chunk.strip():
            chunks.append(self._make_chunk(current_chunk, chunk_id, metadata))

        logger.info(f"Chunked document into {len(chunks)} chunks")
        return chunks

    def chunk_file(self, filepath: str) -> List[Dict]:
        """Chunk a text file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        metadata = {
            "source": os.path.basename(filepath),
            "filepath": filepath
        }
        return self.chunk_text(text, metadata)

    def chunk_directory(self, dir_path: str, extensions: List[str] = None) -> List[Dict]:
        """Chunk all documents in a directory."""
        if extensions is None:
            extensions = ['.txt', '.md', '.csv']

        all_chunks = []
        for filename in os.listdir(dir_path):
            if any(filename.endswith(ext) for ext in extensions):
                filepath = os.path.join(dir_path, filename)
                chunks = self.chunk_file(filepath)
                all_chunks.extend(chunks)
                logger.info(f"Chunked {filename}: {len(chunks)} chunks")

        return all_chunks

    def _make_chunk(self, text: str, chunk_id: int, metadata: Dict = None) -> Dict:
        return {
            "text": text.strip(),
            "chunk_id": chunk_id,
            "char_count": len(text.strip()),
            "metadata": metadata or {}
        }

    def _force_split(self, text: str) -> List[str]:
        """Split oversized text by sentences."""
        sentences = re.split(r'[।\.\!\?]+', text)
        chunks = []
        current = ""
        for sent in sentences:
            sent = sent.strip()
            if not sent:
                continue
            if len(current) + len(sent) < self.char_chunk_size:
                current += (" " + sent if current else sent)
            else:
                if current:
                    chunks.append(current)
                current = sent
        if current:
            chunks.append(current)
        return chunks
