"""
VANI — Intent Classifier
Uses sentence-transformers (MiniLM / DistilBERT) for intent classification.
"""

import os
import json
import logging
import numpy as np
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

INTENT_LABELS = [
    "sales_query", "inventory_query", "invoice_creation",
    "customer_lookup", "employee_query", "attendance_query",
    "report_generation", "reminder", "general_conversation"
]

DATASETS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'datasets', 'intents')


class IntentClassifier:
    """Classifies user text into business intent categories."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.intent_embeddings = {}
        self.intent_labels = INTENT_LABELS

    def load_model(self):
        """Load sentence-transformer model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded model: {self.model_name}")
        except ImportError:
            logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")
            raise

    def load_intent_examples(self, datasets_dir: str = None) -> Dict[str, List[str]]:
        """Load intent examples from JSON dataset files."""
        if datasets_dir is None:
            datasets_dir = DATASETS_DIR

        examples = {}
        for intent in self.intent_labels:
            filepath = os.path.join(datasets_dir, f"{intent}.json")
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                examples[intent] = [item["text"] for item in data]
                logger.info(f"Loaded {len(examples[intent])} examples for '{intent}'")
            else:
                logger.warning(f"Dataset file not found: {filepath}")
                examples[intent] = []
        return examples

    def build_intent_embeddings(self, max_examples_per_intent: int = 100):
        """
        Compute mean embedding for each intent from dataset examples.
        Uses a sample for efficiency.
        """
        if self.model is None:
            self.load_model()

        import random
        examples = self.load_intent_examples()

        for intent, texts in examples.items():
            if not texts:
                continue
            sample = random.sample(texts, min(max_examples_per_intent, len(texts)))
            embeddings = self.model.encode(sample)
            self.intent_embeddings[intent] = np.mean(embeddings, axis=0)
            logger.info(f"Built embedding for '{intent}' from {len(sample)} examples")

    def classify(self, text: str, top_k: int = 3) -> Dict:
        """
        Classify text into an intent.

        Args:
            text: User input text
            top_k: Number of top results to return

        Returns:
            Dict with intent, confidence, and top_k results
        """
        if self.model is None:
            self.load_model()

        if not self.intent_embeddings:
            self.build_intent_embeddings()

        text_embedding = self.model.encode([text])[0]

        # Compute cosine similarity with each intent
        scores = {}
        for intent, intent_emb in self.intent_embeddings.items():
            similarity = np.dot(text_embedding, intent_emb) / (
                np.linalg.norm(text_embedding) * np.linalg.norm(intent_emb)
            )
            scores[intent] = float(similarity)

        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, top_score = sorted_intents[0]

        return {
            "intent": top_intent,
            "confidence": round(top_score, 4),
            "top_k": [{"intent": i, "confidence": round(s, 4)} for i, s in sorted_intents[:top_k]]
        }

    # ═══════════════════════════════════════════
    # TRAINING PLACEHOLDER
    # This section is intentionally left for
    # execution on a separate training machine.
    # Dataset: datasets/intents/*.json
    # Model: sentence-transformers/all-MiniLM-L6-v2
    # or distilbert-base-multilingual-cased
    # Output: ai/nlp/models/intent_classifier_finetuned/
    # ═══════════════════════════════════════════
    def fine_tune(self):
        """Placeholder for fine-tuning on VANI intent dataset."""
        raise NotImplementedError(
            "TRAINING PLACEHOLDER — Execute on training machine. "
            "Dataset: datasets/intents/*.json"
        )
