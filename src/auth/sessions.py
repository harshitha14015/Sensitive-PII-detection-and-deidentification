"""
Session Management Module
Handles user session creation, verification, and cleanup
"""
import sqlite3
import hashlib
import time
from datetime import datetime, timedelta
from config.database import DATABASE_PATH, SESSION_EXPIRY_HOURS

def create_session(username):
    """Create a new session for the user"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Generate session token
    session_token = hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()[:16]
    
    # Set expiration time (24 hours from now) and store as SQLite-friendly string
    expires_at_str = (datetime.now() + timedelta(hours=SESSION_EXPIRY_HOURS)).strftime('%Y-%m-%d %H:%M:%S')
    
    # Save session
    c.execute("INSERT INTO sessions (username, session_token, expires_at) VALUES (?, ?, ?)",
              (username, session_token, expires_at_str))
    
    # Clean up expired sessions
    c.execute("DELETE FROM sessions WHERE expires_at < datetime('now')")
    
    conn.commit()
    conn.close()
    
    return session_token

def verify_session(session_token, username):
    """Verify if a session token is valid"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute("SELECT * FROM sessions WHERE session_token = ? AND username = ? AND expires_at > datetime('now')",
              (session_token, username))
    session = c.fetchone()
    
    conn.close()
    return session is not None

def delete_session(session_token):
    """Delete a session token"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    c.execute("DELETE FROM sessions WHERE session_token = ?", (session_token,))
    conn.commit()
    conn.close()
