"""
Database configuration and settings
"""
import os

# Database settings
DATABASE_PATH = "users.db"

# Default admin credentials
DEFAULT_ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_ENV_VAR = "ADMIN_PASSWORD"

# Session settings
SESSION_EXPIRY_HOURS = 24

# File paths
DATA_DIRECTORY = "data"
UPLOAD_DIRECTORY = os.path.join(DATA_DIRECTORY, "uploads")
PROCESSED_DIRECTORY = os.path.join(DATA_DIRECTORY, "processed")
REPORTS_DIRECTORY = os.path.join(DATA_DIRECTORY, "reports")

# Ensure directories exist
os.makedirs(DATA_DIRECTORY, exist_ok=True)
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
os.makedirs(PROCESSED_DIRECTORY, exist_ok=True)
os.makedirs(REPORTS_DIRECTORY, exist_ok=True)
