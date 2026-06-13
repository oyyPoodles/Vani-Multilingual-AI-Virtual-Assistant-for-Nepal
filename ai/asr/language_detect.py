"""
VANI — Language Detection
Detects Nepali, English, or code-switched (mixed) text.
"""

import re
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

# Unicode ranges for Devanagari script (used by Nepali)
DEVANAGARI_RANGE = re.compile(r'[\u0900-\u097F]')
LATIN_RANGE = re.compile(r'[a-zA-Z]')


def detect_language(text: str) -> Dict[str, any]:
    """
    Detect whether text is Nepali, English, or code-switched.

    Args:
        text: Input text string

    Returns:
        Dict with keys: language, confidence, devanagari_ratio, latin_ratio
    """
    if not text or not text.strip():
        return {"language": "unknown", "confidence": 0.0, "devanagari_ratio": 0, "latin_ratio": 0}

    text = text.strip()
    total_chars = len(re.sub(r'\s+', '', text))

    if total_chars == 0:
        return {"language": "unknown", "confidence": 0.0, "devanagari_ratio": 0, "latin_ratio": 0}

    devanagari_count = len(DEVANAGARI_RANGE.findall(text))
    latin_count = len(LATIN_RANGE.findall(text))

    dev_ratio = devanagari_count / total_chars
    lat_ratio = latin_count / total_chars

    # Classification logic
    if dev_ratio > 0.7:
        language = "ne"  # Nepali
        confidence = min(dev_ratio + 0.1, 1.0)
    elif lat_ratio > 0.7:
        language = "en"  # English
        confidence = min(lat_ratio + 0.1, 1.0)
    elif dev_ratio > 0.1 and lat_ratio > 0.1:
        language = "mixed"  # Code-switched
        confidence = 0.8
    elif dev_ratio > lat_ratio:
        language = "ne"
        confidence = 0.6
    else:
        language = "en"
        confidence = 0.6

    result = {
        "language": language,
        "confidence": round(confidence, 2),
        "devanagari_ratio": round(dev_ratio, 3),
        "latin_ratio": round(lat_ratio, 3)
    }

    logger.debug(f"Language detection: '{text[:50]}...' -> {result}")
    return result


def get_response_language(detected_lang: str, user_preference: str = "auto") -> str:
    """
    Determine response language based on detection and user preference.

    Args:
        detected_lang: Detected language ('ne', 'en', 'mixed')
        user_preference: User's language preference ('ne', 'en', 'auto')

    Returns:
        Language code for response generation
    """
    if user_preference != "auto":
        return user_preference

    if detected_lang == "mixed":
        return "ne"  # Default to Nepali for mixed input
    return detected_lang
