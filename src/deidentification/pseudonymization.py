"""
Pseudo-anonymization Functions for PII De-identification
"""
import random
import string
import re
from config.patterns import TYPE_MAPPING, patterns

# Pseudo-anonymization storage
pseudo_counters = {pii_type: 1 for pii_type in patterns}
pseudo_maps = {pii_type: {} for pii_type in patterns}

def pseudo_anonymize(value, pii_type):
    """Basic pseudo-anonymization with consistent mapping"""
    if value not in pseudo_maps[pii_type]:
        pseudo_maps[pii_type][value] = f"{pii_type}_{pseudo_counters[pii_type]}"
        pseudo_counters[pii_type] += 1
    return pseudo_maps[pii_type][value]

def pseudo_anonymize_pii(pii_type, value):
    """Pseudo-anonymization (fake but realistic values)"""
    # Map the pii_type to the pattern keys
    mapped_type = TYPE_MAPPING.get(pii_type, pii_type.lower())
    
    # Custom pseudo-anonymization for email
    if mapped_type == "email":
        try:
            _, domain = value.strip().split("@")
        except Exception:
            domain = "gmail.com"
        # Generate a consistent fake email for each unique input
        if value not in pseudo_maps["email"]:
            # Use a counter for uniqueness
            pseudo_maps["email"][value] = f"user{pseudo_counters['email']}@{domain}"
            pseudo_counters["email"] += 1
        return pseudo_maps["email"][value]
    else:
        # Use the efficient pseudo_anonymize function for other types
        return pseudo_anonymize(value, mapped_type)

def selective_deidentify(pii_type, value):
    """
    Selective de-identification:
    - Credit Card: mask all but last 4 digits
    - Email: pseudo-anonymize as email1@domain (increment for each unique email, preserve domain)
    - Aadhaar: mask middle 4 digits
    - PAN: anonymize (random string)
    """
    # Initialize static attributes if not present
    if not hasattr(selective_deidentify, "email_map"):
        selective_deidentify.email_map = {}
    if not hasattr(selective_deidentify, "email_counter"):
        selective_deidentify.email_counter = 1

    if pii_type.lower() == "credit_card":
        digits = re.sub(r'\D', '', value)
        if len(digits) < 13:
            return value
        return f"XXXX-XXXX-XXXX-{digits[-4:]}"
    elif pii_type.lower() == "email":
        try:
            _, domain = value.strip().split("@")
        except Exception:
            domain = "gmail.com"
        # Generate a consistent fake email for each unique input
        if value not in selective_deidentify.email_map:
            pseudo_email = f"email{selective_deidentify.email_counter}@{domain}"
            selective_deidentify.email_map[value] = pseudo_email
            selective_deidentify.email_counter += 1
        return selective_deidentify.email_map[value]
    elif pii_type.lower() == "aadhaar":
        digits = re.sub(r'\D', '', value)
        if len(digits) == 12:
            return digits[:4] + "XXXX" + digits[8:]
        return value
    elif pii_type.lower() == "pan":
        # Generate random PAN-like string
        return ''.join(random.choices(string.ascii_uppercase, k=5)) + \
               ''.join(random.choices(string.digits, k=4)) + \
               random.choice(string.ascii_uppercase)
    else:
        return value
