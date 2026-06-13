"""
VANI — Entity Extractor
Extracts dates, customer names, product names, amounts from text.
"""

import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

# Nepali digit mapping
NEPALI_DIGITS = {'०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'}

# Date patterns
DATE_KEYWORDS_NE = {
    "आज": "today", "हिजो": "yesterday", "भोलि": "tomorrow",
    "यो हप्ता": "this_week", "गत हप्ता": "last_week",
    "यो महिना": "this_month", "गत महिना": "last_month",
    "यो बर्ष": "this_year", "गत बर्ष": "last_year"
}

DATE_KEYWORDS_EN = {
    "today": "today", "yesterday": "yesterday", "tomorrow": "tomorrow",
    "this week": "this_week", "last week": "last_week",
    "this month": "this_month", "last month": "last_month",
    "this year": "this_year", "last year": "last_year"
}

AMOUNT_PATTERN = re.compile(r'(?:NPR|Rs\.?|रु\.?)\s*([\d,]+(?:\.\d{2})?)', re.IGNORECASE)
NUMBER_PATTERN = re.compile(r'\b(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\b')
NEPALI_NUMBER_PATTERN = re.compile(r'[०-९]+')


def nepali_to_arabic(text: str) -> str:
    """Convert Nepali digits to Arabic digits."""
    for nep, ara in NEPALI_DIGITS.items():
        text = text.replace(nep, ara)
    return text


class EntityExtractor:
    """Extracts business entities from user text."""

    def extract(self, text: str) -> Dict[str, List]:
        """
        Extract all entities from text.

        Returns:
            Dict with keys: dates, amounts, customers, products, numbers
        """
        return {
            "dates": self._extract_dates(text),
            "amounts": self._extract_amounts(text),
            "customers": self._extract_names(text),
            "products": self._extract_products(text),
            "numbers": self._extract_numbers(text)
        }

    def _extract_dates(self, text: str) -> List[Dict]:
        """Extract date references from text."""
        dates = []
        text_lower = text.lower()

        for keyword, value in {**DATE_KEYWORDS_NE, **DATE_KEYWORDS_EN}.items():
            if keyword in text or keyword in text_lower:
                dates.append({"text": keyword, "value": value})

        # ISO date pattern
        iso_dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
        for d in iso_dates:
            dates.append({"text": d, "value": d})

        return dates

    def _extract_amounts(self, text: str) -> List[Dict]:
        """Extract monetary amounts."""
        amounts = []
        normalized = nepali_to_arabic(text)

        for match in AMOUNT_PATTERN.finditer(normalized):
            val = match.group(1).replace(',', '')
            amounts.append({"text": match.group(0), "value": float(val)})

        return amounts

    def _extract_names(self, text: str) -> List[str]:
        """Extract potential customer/person names."""
        # Simple pattern: look for capitalized words or Nepali name patterns
        name_patterns = [
            re.compile(r'(?:customer|ग्राहक)\s+(\w+)', re.IGNORECASE),
            re.compile(r'(\w+)\s*(?:को|लाई|को)\s', re.IGNORECASE),
            re.compile(r'(?:for|of)\s+(\w+\s?\w*)', re.IGNORECASE),
        ]
        names = []
        for pattern in name_patterns:
            for match in pattern.finditer(text):
                name = match.group(1).strip()
                if len(name) > 1 and name.lower() not in ['the','a','an','को','लाई','मा']:
                    names.append(name)
        return list(set(names))

    def _extract_products(self, text: str) -> List[str]:
        """Extract product mentions."""
        # Common product keywords to look for
        product_keywords = [
            "laptop", "mobile", "phone", "tablet", "rice", "pen", "notebook",
            "cement", "paint", "shirt", "medicine", "keyboard", "mouse",
            "printer", "monitor", "oil", "sugar", "flour"
        ]
        found = []
        text_lower = text.lower()
        for kw in product_keywords:
            if kw in text_lower:
                found.append(kw)
        return found

    def _extract_numbers(self, text: str) -> List[float]:
        """Extract numeric values."""
        normalized = nepali_to_arabic(text)
        numbers = []
        for match in NUMBER_PATTERN.finditer(normalized):
            val = match.group(1).replace(',', '')
            try:
                numbers.append(float(val))
            except ValueError:
                pass
        return numbers
