"""
Database Management Module
Handles SQLite database operations
"""
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timezone, timedelta
from config.database import DATABASE_PATH, DEFAULT_ADMIN_USERNAME, ADMIN_PASSWORD_ENV_VAR

def get_ist_time():
    """Get current time in Indian Standard Time"""
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

def init_db():
    """Initialize SQLite database for user authentication"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT UNIQUE, 
                  password TEXT)''')
    
    # Create admin user if not exists
    c.execute("SELECT 1 FROM users WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    if c.fetchone() is None:
        # Prefer environment variable; otherwise generate a strong random password
        admin_plain = os.getenv(ADMIN_PASSWORD_ENV_VAR)
        if not admin_plain:
            admin_plain = secrets.token_urlsafe(12)
            print(f"[SECURITY NOTICE] Admin user created with temporary password: {admin_plain}")
        
        admin_password_hash = hashlib.sha256(admin_plain.encode()).hexdigest()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (DEFAULT_ADMIN_USERNAME, admin_password_hash))
        except sqlite3.IntegrityError:
            pass  # Race or already exists
    
    # De-identified data history table
    c.execute('''CREATE TABLE IF NOT EXISTS deidentified_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  filename TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  filepath TEXT)''')
    
    # Uploaded data tracking table
    c.execute('''CREATE TABLE IF NOT EXISTS uploaded_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  original_filename TEXT,
                  file_size INTEGER,
                  row_count INTEGER,
                  column_count INTEGER,
                  upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  original_data_path TEXT)''')
    
    # Access logs table
    c.execute('''CREATE TABLE IF NOT EXISTS access_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  action TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Sessions table
    c.execute('''CREATE TABLE IF NOT EXISTS sessions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  session_token TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                  expires_at DATETIME)''')
    
    # Add original_data_path column if it doesn't exist (for existing databases)
    try:
        c.execute("ALTER TABLE uploaded_data ADD COLUMN original_data_path TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

def create_user(username, password):
    """Create a new user with hashed password"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Hash the provided password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
              (username, hashed_password))
    user = c.fetchone()
    conn.close()
    
    return user is not None

def get_all_users():
    """Get all users from the database (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users")
    users = c.fetchall()
    conn.close()
    return users

def delete_user(user_id):
    """Delete a user from the database (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    deleted = conn.total_changes > 0
    conn.close()
    return deleted
