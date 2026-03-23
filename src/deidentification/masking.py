"""
Masking Functions for PII De-identification
"""
import re

def mask_aadhaar(aadhaar):
    """Mask Aadhaar number showing only first 4 and last 4 digits"""
    return aadhaar[:4] + "-XXXX-" + aadhaar[-4:] if len(re.sub(r"\D", "", aadhaar)) == 12 else aadhaar

def mask_pan(pan):
    """Mask PAN showing only first 5 and last 1 characters"""
    return pan[:5] + "****" + pan[-1:] if len(pan) == 10 else pan

def mask_credit_card(card_number: str) -> str:
    """Masks a credit card number, revealing only the last four digits."""
    digits_only = re.sub(r'[^0-9]', '', card_number)  # remove spaces/dashes
    if len(digits_only) < 13:  # Not a valid card length
        return card_number
    return f"XXXX-XXXX-XXXX-{digits_only[-4:]}"

def mask_email(email):
    """Mask email username part"""
    try: 
        u, d = email.split("@")
        return "x"*len(u) + "@" + d
    except: 
        return email

def mask_phone(phone):
    """Mask phone number showing only last 4 digits"""
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return "XXXXXX" + digits[-4:]
    return "XXXXXXXXXX"
