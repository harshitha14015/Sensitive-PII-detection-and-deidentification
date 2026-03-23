"""
PII Detection Module
Handles detection of various PII types in text data
"""
import re
from config.patterns import patterns

def detect_pii(text):
    """Detect PII in text using the compiled patterns"""
    results = []
    safe_text = text or ""
    
    # Collect matches with spans for overlap resolution
    span_results = []  # (type, value, start, end)
    for pii_type, pattern in patterns.items():
        for m in pattern.finditer(safe_text):
            span_results.append((pii_type, m.group(0), m.start(), m.end()))

    if not span_results:
        return []

    # Never classify pure 12-digit sequences as credit cards
    span_results = [
        (t, v, s, e)
        for (t, v, s, e) in span_results
        if not (t == "credit_card" and len(re.sub(r"\D", "", v)) == 12)
    ]

    # Drop Aadhaar matches that are fully contained within any credit card match span
    credit_spans = [(s, e) for (t, _v, s, e) in span_results if t == "credit_card"]
    filtered_spans = []
    for (t, v, s, e) in span_results:
        if t == "aadhaar" and any(s >= cs and e <= ce for (cs, ce) in credit_spans):
            continue
        filtered_spans.append((t, v, s, e))

    # Also, if exact same string was detected as both types, prefer the more specific one
    # Here, prefer credit_card over aadhaar only when strings are identical
    values_by_type = {}
    for (t, v, _s, _e) in filtered_spans:
        values_by_type.setdefault(v, set()).add(t)
    final_list = []
    for (t, v, _s, _e) in filtered_spans:
        types_for_v = values_by_type.get(v, set())
        if "credit_card" in types_for_v and "aadhaar" in types_for_v:
            if t == "aadhaar":
                continue
        final_list.append((t, v))

    return final_list

def _normalize_match_value(raw_value):
    """Normalize regex match values to a string.
    Handles cases where a tuple (full match, groups) may be passed inadvertently.
    """
    if raw_value is None:
        return ""
    if isinstance(raw_value, tuple):
        for part in raw_value:
            if isinstance(part, str) and part:
                return part
        return "".join(str(p) for p in raw_value if p)
    return str(raw_value)

def any_true_pii(text: str) -> bool:
    """Ground truth check: does the text contain any VALID PII?
    Uses validators (e.g., Verhoeff, Luhn) rather than regex alone.
    """
    if not text:
        return False
    
    # Import here to avoid circular imports
    from validation.validators import is_valid_pii
    
    for pii_type, match in detect_pii(text):
        if is_valid_pii(pii_type, match):
            return True
    return False
