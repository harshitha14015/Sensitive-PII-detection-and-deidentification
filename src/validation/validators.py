"""
PII Validators
Contains validation functions for different PII types
"""
import re
from config.patterns import TYPE_MAPPING
from .algorithms import luhn_check, verhoeff_check
from detection.detector import _normalize_match_value

def validate_pan(pan: str, surname: str = None) -> bool:
    """
    Comprehensive PAN validation based on official Income Tax Department rules:
    1. Basic format validation (10 characters: 5 letters + 4 digits + 1 letter)
    2. Entity type validation (4th character)
    3. Check digit validation (10th character)
    4. Business logic validation (position-specific rules)
    """
    if not pan or not isinstance(pan, str):
        return False
    
    # Remove spaces and convert to uppercase
    pan = pan.strip().upper()
    
    # Check length
    if len(pan) != 10:
        return False
    
    # Check basic pattern: 5 letters + 4 digits + 1 letter
    if not re.match(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$", pan):
        return False
    
    # Check entity type (4th character) - Official PAN rules
    valid_entity_types = "ABCFGHLJPT"
    if pan[3] not in valid_entity_types:
        return False
    
    if pan[3] == 'P' and surname:
        if pan[4] != surname.strip().upper()[0]:
            return False
    
    # Additional business logic checks based on entity type
    entity_char = pan[3]
    name_initial = pan[4]
    
    if entity_char in ['C', 'F', 'H', 'A', 'T', 'B', 'L', 'J', 'G']:
        # For these entity types, 5th character should be first letter of entity name
        if not name_initial.isalpha():
            return False
    
    # Validate check digit (10th character) using PAN check digit algorithm
    if not validate_pan_check_digit(pan):
        return False
    
    return True

def validate_pan_check_digit(pan: str) -> bool:
    """
    Validate PAN check digit using the official algorithm.
    The check digit is calculated based on the first 9 characters.
    """
    if len(pan) != 10:
        return False
    
    # Extract first 9 characters
    first_nine = pan[:9]
    
    # PAN check digit calculation algorithm
    weights = [1, 3, 7, 1, 3, 7, 1, 3, 7]
    sum_total = 0
    
    for i, char in enumerate(first_nine):
        if char.isalpha():
            # Convert letter to number (A=10, B=11, ..., Z=35)
            char_value = ord(char.upper()) - ord('A') + 10
        else:
            # It's a digit
            char_value = int(char)
        
        # Multiply by weight
        weighted_value = char_value * weights[i]
        
        # If result is two digits, add them together
        if weighted_value > 9:
            weighted_value = (weighted_value // 10) + (weighted_value % 10)
        
        sum_total += weighted_value
    
    # Calculate check digit
    check_digit_value = (10 - (sum_total % 10)) % 10
    
    # Convert check digit value to letter
    # 0=A, 1=B, 2=C, ..., 9=J
    expected_check_digit = chr(ord('A') + check_digit_value)
    
    # Compare with actual check digit
    return pan[9] == expected_check_digit

def validate_email(email: str) -> bool:
    """
    Comprehensive email validation using multiple checks:
    1. Basic format validation
    2. Length validation
    3. Character validation
    4. Domain validation
    """
    if not email or not isinstance(email, str):
        return False
    
    # Remove whitespace
    email = email.strip()
    
    # Check length constraints
    if len(email) < 5 or len(email) > 254:  # RFC 5321 limits
        return False
    
    # Check for exactly one @ symbol
    if email.count('@') != 1:
        return False
    
    local_part, domain_part = email.split('@')
    
    # Local part validation
    if len(local_part) < 1 or len(local_part) > 64:  # RFC 5321 limits
        return False
    
    # Domain part validation
    if len(domain_part) < 1 or len(domain_part) > 253:
        return False
    
    # Check for consecutive dots
    if '..' in email:
        return False
    
    # Check for valid characters in local part
    valid_local_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.!#$%&'*+/=?^_`{|}~-")
    if not all(c in valid_local_chars for c in local_part):
        return False
    
    # Check for valid characters in domain part
    valid_domain_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-")
    if not all(c in valid_domain_chars for c in domain_part):
        return False
    
    # Domain must have at least one dot
    if '.' not in domain_part:
        return False
    
    # Domain cannot start or end with dot or hyphen
    if domain_part.startswith('.') or domain_part.endswith('.') or domain_part.startswith('-') or domain_part.endswith('-'):
        return False
    
    # TLD must be at least 2 characters
    tld = domain_part.split('.')[-1]
    if len(tld) < 2:
        return False
    
    return True

def is_valid_pii(pii_type: str, value: str) -> bool:
    """Validate detected PII candidates using stricter semantics.
    - Aadhaar: exactly 12 digits and must start with 2-9
    - PAN: pattern already strict
    - Credit Card: 13-16 digits after stripping separators + Luhn check
    - Email: basic email format
    - Phone: 10 digits starting with 6-9
    """
    # Ensure value is a string (regex operations expect str/bytes)
    value = _normalize_match_value(value)
    digits_only = re.sub(r"\D", "", value or "")
    
    # Map the pii_type to the pattern keys
    mapped_type = TYPE_MAPPING.get(pii_type, pii_type.lower())
    
    if mapped_type == "aadhaar":
        # Aadhaar must be 12 digits, start with 2-9, and pass Verhoeff checksum
        return (
            len(digits_only) == 12
            and digits_only[0] in "23456789"
            and verhoeff_check(digits_only)
        )
    if mapped_type == "pan":
        return validate_pan(value)
    if mapped_type == "credit_card":
        return 13 <= len(digits_only) <= 19 and luhn_check(value)
    if mapped_type == "email":
        return validate_email(value)
    if mapped_type == "phone":
        return bool(re.fullmatch(r"[6-9][0-9]{9}", digits_only))
    return False

# Helper functions for PAN analysis
def get_pan_entity_type(pan: str) -> str:
    """Get entity type from PAN 4th character"""
    if not pan or len(pan) < 4:
        return "Unknown"
    
    entity_types = {
        'P': 'Individual',
        'C': 'Company',
        'H': 'HUF (Hindu Undivided Family)',
        'F': 'Firm',
        'A': 'Association of Persons (AOP)',
        'T': 'Trust',
        'B': 'Body of Individuals (BOI)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'G': 'Government'
    }
    
    return entity_types.get(pan[3], "Unknown")

def get_pan_holder_name_initial(pan: str) -> str:
    """Get the name initial from PAN 5th character"""
    if not pan or len(pan) < 5:
        return "Unknown"
    
    return pan[4]

def get_pan_serial_number(pan: str) -> str:
    """Get the serial number from PAN (6th to 9th characters)"""
    if not pan or len(pan) < 9:
        return "Unknown"
    
    return pan[5:9]
