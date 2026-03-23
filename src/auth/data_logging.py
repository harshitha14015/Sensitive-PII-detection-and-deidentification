"""
Data Logging Module
Handles logging of uploaded data, processed data, and access logs
"""
import sqlite3
import os
from config.database import DATABASE_PATH
from .database import get_ist_time

def save_deidentified_data(username, filename, filepath):
    """Save information about de-identified data"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    ist_time = get_ist_time()
    c.execute("INSERT INTO deidentified_data (username, filename, filepath, timestamp) VALUES (?, ?, ?, ?)",
              (username, filename, filepath, ist_time))
    conn.commit()
    conn.close()

def get_all_deidentified_data():
    """Get all de-identified data records (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, filename, timestamp, filepath FROM deidentified_data ORDER BY timestamp DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_deidentified_data(record_id):
    """Delete a de-identified data record (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Get filepath before deleting
    c.execute("SELECT filepath FROM deidentified_data WHERE id = ?", (record_id,))
    result = c.fetchone()
    filepath = result[0] if result else None
    
    # Delete the record
    c.execute("DELETE FROM deidentified_data WHERE id = ?", (record_id,))
    conn.commit()
    deleted = conn.total_changes > 0
    conn.close()
    
    # Delete the actual file if it exists
    if filepath and os.path.exists(filepath):
        try:
            os.remove(filepath)
        except:
            pass  # Silently fail if file can't be deleted
    
    return deleted

def save_uploaded_data(username, original_filename, file_size, row_count, column_count, original_data_path):
    """Save information about uploaded data"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    ist_time = get_ist_time()
    c.execute("""INSERT INTO uploaded_data 
                 (username, original_filename, file_size, row_count, column_count, original_data_path, upload_timestamp) 
                 VALUES (?, ?, ?, ?, ?, ?, ?)""",
              (username, original_filename, file_size, row_count, column_count, original_data_path, ist_time))
    conn.commit()
    conn.close()

def get_all_uploaded_data():
    """Get all uploaded data records (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("""SELECT id, username, original_filename, file_size, row_count, column_count, 
                        upload_timestamp, original_data_path 
                 FROM uploaded_data ORDER BY upload_timestamp DESC""")
    data = c.fetchall()
    conn.close()
    return data

def delete_uploaded_data(record_id):
    """Delete an uploaded data record (admin only)"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM uploaded_data WHERE id = ?", (record_id,))
    conn.commit()
    deleted = conn.total_changes > 0
    conn.close()
    return deleted

def save_access_log(username: str, action: str):
    """Save access log (login/signup/logout) with timestamp only."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        ist_time = get_ist_time()
        c.execute("INSERT INTO access_logs (username, action, timestamp) VALUES (?, ?, ?)", 
                  (username, action, ist_time))
        conn.commit()
        conn.close()
    except Exception:
        pass

def get_access_logs():
    """Get access logs for non-admin users"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, action, timestamp FROM access_logs WHERE username <> 'admin' ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def delete_all_access_logs():
    """Delete all access logs except admin logs"""
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM access_logs WHERE username <> 'admin'")
    conn.commit()
    count = conn.total_changes
    conn.close()
    return count
