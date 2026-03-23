"""
Main De-identification Handler
Coordinates different de-identification methods
"""
import re
from config.patterns import TYPE_MAPPING
from .masking import mask_aadhaar, mask_pan, mask_credit_card, mask_email, mask_phone
from .anonymization import anonymize_pii
from .pseudonymization import pseudo_anonymize_pii, selective_deidentify

def mask_pii(pii_type, value):
    """Mask PII using standard masking rules"""
    mapped_type = TYPE_MAPPING.get(pii_type, pii_type.lower())
    
    if mapped_type == "aadhaar":
        return mask_aadhaar(value)
    elif mapped_type == "pan":
        return mask_pan(value)
    elif mapped_type == "credit_card":
        return mask_credit_card(value)
    elif mapped_type == "email":
        return mask_email(value)
    elif mapped_type == "phone":
        return mask_phone(value)
    else:
        return value

def deidentify_value(method, pii_type, value):
    """Apply the specified de-identification method to a value"""
    if method == "Masking":
        return mask_pii(pii_type, value)
    elif method == "Anonymization":
        return anonymize_pii(pii_type, value)
    elif method == "Pseudo-Anonymization":
        return pseudo_anonymize_pii(pii_type, value)
    elif method == "Selective":
        return selective_deidentify(pii_type, value)
    else:
        return value
