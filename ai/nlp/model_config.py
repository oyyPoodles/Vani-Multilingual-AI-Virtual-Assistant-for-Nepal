"""
VANI — NLP Model Configuration
Central config for all NLP models used in the pipeline.
"""

# Intent Classification Model
INTENT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INTENT_MODEL_BACKUP = "distilbert-base-multilingual-cased"

# Entity Recognition (future fine-tuning)
NER_MODEL = "xlm-roberta-base"

# Embedding Model for RAG
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Language Detection
LANG_DETECT_MODEL = "papluca/xlm-roberta-base-language-detection"

# Confidence Thresholds
INTENT_CONFIDENCE_THRESHOLD = 0.5
ENTITY_CONFIDENCE_THRESHOLD = 0.6

# Max sequence lengths
MAX_INPUT_LENGTH = 512
MAX_CONTEXT_LENGTH = 2048

# Supported languages
SUPPORTED_LANGUAGES = ["ne", "en", "mixed"]

# Intent labels
INTENT_LABELS = [
    "sales_query",
    "inventory_query",
    "invoice_creation",
    "customer_lookup",
    "employee_query",
    "attendance_query",
    "report_generation",
    "reminder",
    "general_conversation"
]
