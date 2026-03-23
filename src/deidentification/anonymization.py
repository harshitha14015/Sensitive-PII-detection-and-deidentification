"""
Anonymization Functions for PII De-identification
"""
import random
import string
from config.patterns import TYPE_MAPPING

def anonymize_pii(pii_type, value):
    """Full anonymization for sensitive data"""
    # Map the pii_type to the pattern keys
    mapped_type = TYPE_MAPPING.get(pii_type, pii_type.lower())
    
    def random_string(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    if mapped_type == "credit_card":
        # Generate a random 16-digit string
        return random_string(16)
    elif mapped_type == "email":
        # Generate a random email
        return f"{random_string(8)}@{random_string(5)}.com"
    elif mapped_type == "aadhaar":
        # Generate a random 12-digit string
        return random_string(12)
    elif mapped_type == "pan":
        # Generate a random PAN-like string
        return random_string(5).upper() + random_string(4) + random_string(1).upper()
    elif mapped_type == "phone":
        # Generate a random 10-digit string starting with 9
        return "9" + random_string(9)
    else:
        return random_string(10)
