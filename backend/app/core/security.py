"""
Security helpers for ResuM8.
Includes data masking, encryption utilities, and auto-delete helpers.
"""
import hashlib
import base64
import re
from cryptography.fernet import Fernet
from app.core.config import settings


def get_fernet_key() -> bytes:
    """Derive a Fernet-compatible key from the SECRET_KEY setting."""
    # Hash the secret key to get exactly 32 bytes, then base64url-encode it
    key_bytes = hashlib.sha256(settings.secret_key.encode()).digest()
    return base64.urlsafe_b64encode(key_bytes)


def encrypt_text(plaintext: str) -> str:
    """Encrypt a string using Fernet symmetric encryption."""
    f = Fernet(get_fernet_key())
    return f.encrypt(plaintext.encode()).decode()


def decrypt_text(ciphertext: str) -> str:
    """Decrypt a Fernet-encrypted string."""
    f = Fernet(get_fernet_key())
    return f.decrypt(ciphertext.encode()).decode()


def mask_name(full_name: str) -> str:
    """
    Mask a candidate's name for bias-free recruiter review.
    E.g. 'John Smith' -> 'J*** S****'
    """
    if not full_name:
        return "Candidate"
    parts = full_name.strip().split()
    masked = []
    for part in parts:
        if len(part) <= 1:
            masked.append(part)
        else:
            masked.append(part[0] + "*" * (len(part) - 1))
    return " ".join(masked)


def mask_email(email: str) -> str:
    """
    Mask an email address for privacy.
    E.g. 'john.smith@email.com' -> 'j***@*****.com'
    """
    if not email or "@" not in email:
        return "***@***.***"
    local, domain = email.split("@", 1)
    masked_local = local[0] + "***" if local else "***"
    domain_parts = domain.rsplit(".", 1)
    if len(domain_parts) == 2:
        masked_domain = "*****." + domain_parts[1]
    else:
        masked_domain = "*****"
    return f"{masked_local}@{masked_domain}"


def mask_phone(phone: str) -> str:
    """
    Mask a phone number, showing only last 4 digits.
    E.g. '+1-555-123-4567' -> '***-***-4567'
    """
    if not phone:
        return "***-***-****"
    # Keep only last 4 digits
    digits = re.sub(r'\D', '', phone)
    if len(digits) >= 4:
        return "***-***-" + digits[-4:]
    return "***-***-****"


def apply_data_masking(candidate_data: dict) -> dict:
    """
    Apply all data masking to a candidate dict.
    Returns a new dict with sensitive fields masked.
    """
    masked = candidate_data.copy()
    if "name" in masked:
        masked["name"] = mask_name(masked["name"])
    if "email" in masked:
        masked["email"] = mask_email(masked["email"])
    if "phone" in masked:
        masked["phone"] = mask_phone(masked["phone"])
    return masked


def sanitize_filename(filename: str) -> str:
    """Remove unsafe characters from uploaded filenames."""
    # Allow only alphanumeric, dash, underscore, dot
    sanitized = re.sub(r'[^\w\-.]', '_', filename)
    # Prevent path traversal
    sanitized = sanitized.replace('..', '_')
    return sanitized[:255]  # Limit length
