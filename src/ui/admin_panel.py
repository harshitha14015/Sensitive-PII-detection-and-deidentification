"""
Admin Panel UI Components
"""
import streamlit as st
import time
import os
from auth.database import get_all_users, delete_user
from auth.data_logging import (
    get_all_uploaded_data, delete_uploaded_data,
    get_all_deidentified_data, delete_deidentified_data,
    get_access_logs, delete_all_access_logs, save_access_log
)
from auth.sessions import delete_session

def show_admin_panel():
    """Display admin panel with user management and data access"""
    st.title("Admin Panel")
    
    # Logout button
    if st.button("Logout", key="admin_logout"):
        try:
            save_access_log(st.session_state.get('username', 'Unknown'), "Logout")
        except Exception:
            pass
        
        # Delete session from database
        if st.session_state.get('session_token'):
            delete_session(st.session_state.session_token)
        
        # Clear session state and redirect to clean URL
        st.session_state.logged_in = False
        st.session_state.pop('username', None)
        st.session_state.pop('session_token', None)
        
        # Redirect to clean URL without parameters
        st.markdown("""
        <script>
        // Redirect to clean URL
        const currentUrl = window.location.href.split('?')[0];
        window.location.href = currentUrl;
        </script>
        """, unsafe_allow_html=True)
        st.stop()
    
    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(["User Management", "Uploaded Data", "Processed Data", "User Logs"])
    
    with admin_tab1:
        _show_user_management()
    
    with admin_tab2:
        _show_uploaded_data_management()
    
    with admin_tab3:
        _show_processed_data_management()
    
    with admin_tab4:
        _show_access_logs()

def _show_user_management():
    """Show user management section"""
    st.write("User Management")
    users = get_all_users()
    
    st.write("Registered Users:")
    for user in users:
        col1, col2, col3 = st.columns([3, 5, 2])
        with col1:
            st.write(f"ID: {user[0]}")
        with col2:
            st.write(f"Username: {user[1]}")
        with col3:
            if user[1] != "admin":  # Prevent deleting the admin account
                if st.button("Delete", key=f"delete_{user[0]}"):
                    if delete_user(user[0]):
                        st.success(f"User {user[1]} deleted!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to delete user")

def _show_uploaded_data_management():
    """Show uploaded data management section"""
    # Get uploaded data first
    uploaded_records = get_all_uploaded_data()
    
    # Bulk actions for uploaded data
    colA, colB = st.columns([3, 1])
    with colA:
        st.write("**Uploaded Data Records**")
    with colB:
        if st.button("🧹 Clear All Uploaded Data", key="clear_all_uploaded"):
            if uploaded_records:
                # Delete all uploaded data records
                import sqlite3
                from config.database import DATABASE_PATH
                conn = sqlite3.connect(DATABASE_PATH)
                c = conn.cursor()
                c.execute("DELETE FROM uploaded_data")
                deleted_count = conn.total_changes
                conn.commit()
                conn.close()
                
                # Delete all original data files
                files_deleted = 0
                for record in uploaded_records:
                    if record[7] and os.path.exists(record[7]):  # original_data_path
                        try:
                            os.remove(record[7])
                            files_deleted += 1
                        except:
                            pass
                
                st.success(f"Cleared {deleted_count} uploaded data records and {files_deleted} files.")
                time.sleep(1)
                st.rerun()
            else:
                st.info("No uploaded data to clear.")
    
    if not uploaded_records:
        st.info("No uploaded data found.")
    else:
        for record in uploaded_records:
            with st.expander(f"{record[2]} - {record[1]} ({record[6].split()[0]})", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**User:** {record[1]}")
                    st.write(f"**File:** {record[2]}")
                    st.write(f"**Size:** {record[3] / 1024:.1f} KB")
                    st.write(f"**Rows:** {record[4]}, **Columns:** {record[5]}")
                    st.write(f"**Uploaded:** {record[6]} IST")
                
                with col2:
                    if record[7] and os.path.exists(record[7]):  # original_data_path
                        with open(record[7], "rb") as f:
                            st.download_button("Download Original", f, file_name=record[2], key=f"dl_orig_{record[0]}")
                    else:
                        st.write("File not available")
                    
                    if st.button("🗑️ Delete", key=f"del_upload_{record[0]}", use_container_width=True):
                        if delete_uploaded_data(record[0]):
                            # Also delete the file if it exists
                            if record[7] and os.path.exists(record[7]):
                                try:
                                    os.remove(record[7])
                                except:
                                    pass
                            st.success("Upload record deleted!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("Failed to delete record")

def _show_processed_data_management():
    """Show processed data management section"""
    # Get processed data first
    data_records = get_all_deidentified_data()
    
    # Bulk actions for processed data
    colA, colB = st.columns([3, 1])
    with colA:
        st.write("**De-identified Data Records**")
    with colB:
        if st.button("🧹 Clear All Processed Data", key="clear_all_processed"):
            if data_records:
                # Delete all processed data records
                import sqlite3
                from config.database import DATABASE_PATH
                conn = sqlite3.connect(DATABASE_PATH)
                c = conn.cursor()
                c.execute("DELETE FROM deidentified_data")
                deleted_count = conn.total_changes
                conn.commit()
                conn.close()
                
                # Delete all processed data files
                files_deleted = 0
                for record in data_records:
                    if record[4] and os.path.exists(record[4]):  # filepath
                        try:
                            os.remove(record[4])
                            files_deleted += 1
                        except:
                            pass
                
                st.success(f"Cleared {deleted_count} processed data records and {files_deleted} files.")
                time.sleep(1)
                st.rerun()
            else:
                st.info("No processed data to clear.")
    
    if not data_records:
        st.info("No de-identified data records found.")
    else:
        for record in data_records:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 3, 2, 2])
            with col1:
                st.write(f"ID: {record[0]}")
            with col2:
                st.write(f"User: {record[1]}")
            with col3:
                st.write(f"File: {record[2]}")
            with col4:
                st.write(f"Time: {record[3]} IST")
            with col5:
                if os.path.exists(record[4]):
                    with open(record[4], "rb") as f:
                        st.download_button("Download", f, file_name=record[2], key=f"dl_{record[0]}")
                else:
                    st.write("File missing")
            with col6:
                if st.button("Delete", key=f"del_data_{record[0]}"):
                    if delete_deidentified_data(record[0]):
                        st.success("Record deleted!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Failed to delete record")

def _show_access_logs():
    """Show access logs section"""
    st.write("**Access Logs (Admin only)**")
    colA, colB = st.columns([3, 1])

    with colA:
        st.caption("Login/Signup/Logout with timestamps")

    with colB:
        if st.button("🧹 Clear All Access Logs", key="clear_access_logs"):
            count = delete_all_access_logs()
            st.success(f"Cleared {count} access logs.")
            time.sleep(1)
            st.rerun()

    logs = get_access_logs()
    filtered_logs = [log for log in logs if log[2] in ("Signup", "Login", "Logout")]

    if not filtered_logs:
        st.info("No access logs found.")
    else:
        st.write("**Recent User Activities:**")
        for log in filtered_logs:
            st.write(f" {log[3]} —  {log[1]} —  {log[2]}")
