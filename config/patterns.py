"""
PII Detection Patterns Configuration
Contains regex patterns for various PII types
"""
import re

# ===================== PII DETECTION PATTERNS =====================
patterns = {
    # Aadhaar: exactly 12 digits, optional consistent separators, no leading/trailing digits
    # Detection is broad (allows 0/1 starts) so invalid ones are treated as false positives by validators
    # Matches either 12 contiguous digits or 4-4-4 with same separator (space or dash)
    "aadhaar": re.compile(r"(?<!\d)(?:\d{12}|(\d{4})([\-\s])\d{4}\2\d{4})(?![\d-])"),
    
    # Enhanced PAN pattern with word boundaries for better detection
    "pan": re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b"),
    
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
    
    # RFC 5322 compliant email pattern (more comprehensive)
    "email": re.compile(r"\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\b"),
    
    "phone": re.compile(r"\b[6-9]\d{9}\b")
}

# Type mapping for UI display names to internal pattern keys
TYPE_MAPPING = {
    "Credit Card": "credit_card",
    "Email": "email", 
    "Aadhaar": "aadhaar",
    "PAN": "pan",
    "Phone": "phone"
}
