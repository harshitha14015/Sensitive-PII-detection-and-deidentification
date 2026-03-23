"""
Main Streamlit Application
PII Detection and De-identification Tool
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import hashlib
import time
import re
import math
import os
import sys

# Add the src directory to the Python path
sys.path.append('src')

# Import modules
from config.patterns import patterns
from detection.detector import detect_pii, any_true_pii
from validation.validators import is_valid_pii
from deidentification.deidentifier import deidentify_value
from auth.database import init_db
from auth.sessions import verify_session, delete_session
from auth.data_logging import save_uploaded_data, save_deidentified_data, save_access_log
from reports.pdf_generator import generate_accuracy_report_pdf
from ui.styling import apply_custom_css
from ui.login import show_login_page
from ui.admin_panel import show_admin_panel

def main_app():
    """Main application interface for regular users"""
    st.set_page_config(page_title="PII De-Identification Tool", layout="wide", initial_sidebar_state="expanded")
    
    # Apply custom CSS
    apply_custom_css()
    
    # If admin, show full screen admin panel
    if st.session_state.username == "admin":
        show_admin_panel()
        return
    
    # Enhanced main title
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   background-clip: text; font-size: 2.5rem; margin-bottom: 0.5rem;">
            Sensitive PII Detection & De-Identification Tool
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar with user info
    with st.sidebar:
        st.markdown("### User Dashboard")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <p style="margin: 0; font-weight: 600; color: #495057;">
                Welcome, <strong>{st.session_state.username}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
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

        # Add some helpful info
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.info("**Tip**: Upload CSV files to detect and anonymize PII data automatically")

    # File Upload Section
    st.markdown("### Upload Your Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file to analyze", 
        type=["csv"],
        help="Upload a CSV file containing data you want to scan for PII"
    )

    if uploaded_file:
        # Process uploaded file
        process_uploaded_file(uploaded_file)
    else:
        # Show empty state
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0; color: #666;">
            <h3>Ready to Analyze Your Data</h3>
            <p style="font-size: 1.1rem; margin: 1rem 0;">
                Upload a CSV file to begin PII detection and de-identification
            </p>
            <p style="color: #999;">
                Supported formats: CSV files with text data
            </p>
        </div>
        """, unsafe_allow_html=True)

def process_uploaded_file(uploaded_file):
    """Process the uploaded CSV file"""
    # Ensure we only persist an uploaded file once across Streamlit reruns
    if 'processed_upload_hashes' not in st.session_state:
        st.session_state.processed_upload_hashes = set()

    # Read bytes and hash to identify this exact content
    file_bytes = uploaded_file.getvalue()
    file_hash = hashlib.sha256(file_bytes).hexdigest()

    # Build DataFrame from in-memory bytes (safe for repeated reruns)
    df = pd.read_csv(io.BytesIO(file_bytes))

    if file_hash not in st.session_state.processed_upload_hashes:
        # Save original data for admin access
        original_data_path = f"Original_Data_{st.session_state.username}_{int(time.time())}.csv"
        df.to_csv(original_data_path, index=False)

        # Save upload info to database
        save_uploaded_data(
            username=st.session_state.username,
            original_filename=uploaded_file.name,
            file_size=uploaded_file.size,
            row_count=len(df),
            column_count=len(df.columns),
            original_data_path=original_data_path
        )

        # Log the upload action
        save_access_log(st.session_state.username, f"Uploaded: {uploaded_file.name}")

        # Mark processed so subsequent reruns don't duplicate
        st.session_state.processed_upload_hashes.add(file_hash)
    
    # Show data preview
    show_data_preview(df, uploaded_file)
    
    # Process data for PII detection
    process_data_for_pii(df)

def show_data_preview(df, uploaded_file):
    """Display data preview with loading animation"""
    st.markdown("### Data Preview")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("Processing uploaded data...")
    progress_bar.progress(25)
    time.sleep(0.5)
    
    status_text.text("Analyzing data structure...")
    progress_bar.progress(50)
    time.sleep(0.5)
    
    status_text.text("Data loaded successfully!")
    progress_bar.progress(100)
    time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()
    
    # Show data info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", len(df))
    with col2:
        st.metric("Columns", len(df.columns))
    with col3:
        st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
    
    st.dataframe(df, use_container_width=True)

def process_data_for_pii(df):
    """Process data for PII detection and de-identification"""
    # Method Selection
    st.markdown("### Choose De-identification Method")
    method = st.radio(
        "Select your preferred de-identification approach:",
        ["Masking", "Anonymization", "Pseudo-Anonymization", "Selective"],
        horizontal=True,
        help="Masking: Hide parts of PII (XXXX). Anonymization: Replace with random strings. Pseudo-Anonymization: Replace with consistent fake values. Selective: Use field-specific rules."
    )
    
    # Process the data
    deidentified_data, metrics, metric_data, pii_detection_summary = analyze_dataframe(df, method)
    
    # Show results
    show_results(deidentified_data, metrics, metric_data, pii_detection_summary)

def analyze_dataframe(df, method):
    """Analyze DataFrame for PII and apply de-identification"""
    deidentified_data = df.copy()
    pii_detection_summary = {}
    
    # Initialize metrics and data storage
    metrics = {'TP': 0, 'TN': 0, 'FP': 0, 'FN': 0}
    metric_data = {'TP': [], 'TN': [], 'FP': [], 'FN': []}
    
    # Process each cell
    for col in df.columns:
        for idx, value in enumerate(df[col].astype(str)):
            detections = detect_pii(value)
            has_ground_truth = any_true_pii(value)
            has_detection = bool(detections)

            # Update metrics
            if has_detection:
                valid_detection = False
                for pii_type, match in detections:
                    if is_valid_pii(pii_type, match):
                        valid_detection = True
                        break
                
                if valid_detection and has_ground_truth:
                    metrics['TP'] += 1
                    valid_detections = [d for d in detections if is_valid_pii(d[0], d[1])]
                    metric_data['TP'].append((idx, col, value, valid_detections))
                elif valid_detection and not has_ground_truth:
                    metrics['FP'] += 1
                    valid_detections = [d for d in detections if is_valid_pii(d[0], d[1])]
                    metric_data['FP'].append((idx, col, value, valid_detections))
                elif not valid_detection and has_ground_truth:
                    metrics['FN'] += 1
                    metric_data['FN'].append((idx, col, value, "Actual PII present but not detected"))
                else:
                    metrics['FP'] += 1
                    valid_detections = [d for d in detections if is_valid_pii(d[0], d[1])]
                    metric_data['FP'].append((idx, col, value, valid_detections))
            else:
                if has_ground_truth:
                    metrics['FN'] += 1
                    metric_data['FN'].append((idx, col, value, "Actual PII present but not detected"))
                else:
                    metrics['TN'] += 1
                    metric_data['TN'].append((idx, col, value))

            # Apply de-identification
            if has_detection:
                original_value = value
                detections.sort(key=lambda x: len(x[1]), reverse=True)
                replaced_matches = set()
                
                for pii_type, match in detections:
                    if any(match in rm for rm in replaced_matches):
                        continue
                    
                    if not is_valid_pii(pii_type, match):
                        continue
                    
                    deidentified_value = deidentify_value(method, pii_type, match)
                    pattern = re.escape(match)
                    original_value = re.sub(pattern, deidentified_value, original_value)
                    replaced_matches.add(match)
                    
                    # Update summary by column
                    pii_detection_summary[col] = pii_detection_summary.get(col, 0) + 1
                
                deidentified_data.at[idx, col] = original_value
            else:
                deidentified_data.at[idx, col] = value
    
    return deidentified_data, metrics, metric_data, pii_detection_summary

def show_results(deidentified_data, metrics, metric_data, pii_detection_summary):
    """Display the results of PII detection and de-identification"""
    # Show de-identified data
    st.markdown("### De-Identified Data Preview")
    st.success("PII detection and de-identification completed successfully!")
    st.dataframe(deidentified_data, use_container_width=True)
    
    # Show metrics
    show_detection_metrics(metrics, metric_data)
    
    # Show performance analysis
    show_performance_analysis(metrics)
    
    # Show download options
    show_download_options(deidentified_data, metrics, pii_detection_summary)
    
    # Show PII summary
    show_pii_summary(pii_detection_summary)

def show_detection_metrics(metrics, metric_data):
    """Display detection performance metrics"""
    st.markdown("### Detection Performance Metrics")
    st.markdown("**Click on any metric below to view detailed data:**")

    # Initialize session state for metric visibility
    for metric_type in ['tp', 'tn', 'fp', 'fn']:
        if f'show_{metric_type}' not in st.session_state:
            st.session_state[f'show_{metric_type}'] = False
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        from ui.styling import create_metric_card
        st.markdown(create_metric_card("True Positives", metrics['TP'], "Correctly detected PII", "tp"), unsafe_allow_html=True)
        if st.button(f"{'Hide Details' if st.session_state.show_tp else 'View Details'}", key="tp_button", use_container_width=True):
            # Close all others and toggle current
            for other in ['tn', 'fp', 'fn']:
                st.session_state[f'show_{other}'] = False
            st.session_state.show_tp = not st.session_state.show_tp
            st.rerun()
    
    with col2:
        st.markdown(create_metric_card("True Negatives", metrics['TN'], "Correctly ignored non-PII", "tn"), unsafe_allow_html=True)
        if st.button(f"{'Hide Details' if st.session_state.show_tn else 'View Details'}", key="tn_button", use_container_width=True):
            for other in ['tp', 'fp', 'fn']:
                st.session_state[f'show_{other}'] = False
            st.session_state.show_tn = not st.session_state.show_tn
            st.rerun()
    
    with col3:
        st.markdown(create_metric_card("False Positives", metrics['FP'], "Incorrectly flagged non-PII", "fp"), unsafe_allow_html=True)
        if st.button(f"{'Hide Details' if st.session_state.show_fp else 'View Details'}", key="fp_button", use_container_width=True):
            for other in ['tp', 'tn', 'fn']:
                st.session_state[f'show_{other}'] = False
            st.session_state.show_fp = not st.session_state.show_fp
            st.rerun()
    
    with col4:
        st.markdown(create_metric_card("False Negatives", metrics['FN'], "Missed PII", "fn"), unsafe_allow_html=True)
        if st.button(f"{'Hide Details' if st.session_state.show_fn else 'View Details'}", key="fn_button", use_container_width=True):
            for other in ['tp', 'tn', 'fp']:
                st.session_state[f'show_{other}'] = False
            st.session_state.show_fn = not st.session_state.show_fn
            st.rerun()
    
    # Display data based on clicked metrics
    if st.session_state.show_tp and metric_data['TP']:
        st.subheader("True Positives (TP) - Correctly Detected PII")
        tp_df = pd.DataFrame(metric_data['TP'], columns=['Row', 'Column', 'Original Value', 'Detected PII'])
        st.dataframe(tp_df, use_container_width=True)
    
    if st.session_state.show_tn and metric_data['TN']:
        st.subheader("True Negatives (TN) - Correctly Ignored Non-PII")
        tn_df = pd.DataFrame(metric_data['TN'], columns=['Row', 'Column', 'Original Value'])
        st.dataframe(tn_df, use_container_width=True)
    
    if st.session_state.show_fp and metric_data['FP']:
        st.subheader("False Positives (FP) - Incorrectly Flagged Non-PII")
        fp_df = pd.DataFrame(metric_data['FP'], columns=['Row', 'Column', 'Original Value', 'Detected PII'])
        st.dataframe(fp_df, use_container_width=True)
    
    if st.session_state.show_fn and metric_data['FN']:
        st.subheader("False Negatives (FN) - Missed PII")
        fn_df = pd.DataFrame(metric_data['FN'], columns=['Row', 'Column', 'Original Value', 'Issue'])
        st.dataframe(fn_df, use_container_width=True)

def show_performance_analysis(metrics):
    """Display comprehensive performance analysis"""
    # Calculate metrics
    precision = metrics['TP'] / (metrics['TP'] + metrics['FP']) if (metrics['TP'] + metrics['FP']) > 0 else 0
    recall = metrics['TP'] / (metrics['TP'] + metrics['FN']) if (metrics['TP'] + metrics['FN']) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (metrics['TP'] + metrics['TN']) / (metrics['TP'] + metrics['TN'] + metrics['FP'] + metrics['FN']) if (metrics['TP'] + metrics['TN'] + metrics['FP'] + metrics['FN']) > 0 else 0
    specificity = metrics['TN'] / (metrics['TN'] + metrics['FP']) if (metrics['TN'] + metrics['FP']) > 0 else 0
    
    st.subheader("Comprehensive Accuracy Analysis")

    # Show metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Accuracy", f"{accuracy:.2%}", help="Percentage of correct predictions")
    with col2:
        st.metric("Precision", f"{precision:.2%}", help="Percentage of positive predictions that were correct")
    with col3:
        st.metric("Recall (Sensitivity)", f"{recall:.2%}", help="Percentage of actual positives correctly identified")
    with col4:
        st.metric("Specificity", f"{specificity:.2%}", help="Percentage of actual negatives correctly identified")
    
    # Additional metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("F1-Score", f"{f1_score:.2%}", help="Balanced measure of precision and recall")
    with col2:
        total_samples = metrics['TP'] + metrics['TN'] + metrics['FP'] + metrics['FN']
        st.metric("Total Samples", f"{total_samples:,}", help="Total number of data points analyzed")
    with col3:
        error_rate = (metrics['FP'] + metrics['FN']) / total_samples if total_samples > 0 else 0
        st.metric("Error Rate", f"{error_rate:.2%}", help="Percentage of incorrect predictions")
    with col4:
        positive_rate = (metrics['TP'] + metrics['FP']) / total_samples if total_samples > 0 else 0
        st.metric("Detection Rate", f"{positive_rate:.2%}", help="Percentage of data points flagged as PII")
    
    # Show visualization
    show_metrics_visualization(metrics, precision, recall, f1_score)

def show_metrics_visualization(metrics, precision, recall, f1_score):
    """Display visualization of metrics"""
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    
    # Metrics bar chart
    metrics_names = ['TP', 'TN', 'FP', 'FN']
    metrics_values = [metrics['TP'], metrics['TN'], metrics['FP'], metrics['FN']]
    colors_list = ['#43e97b', '#4facfe', '#f093fb', '#f5576c']
    bars = ax[0].bar(metrics_names, metrics_values, color=colors_list)
    ax[0].set_title('Detection Metrics', fontsize=14, fontweight='bold', color='#2c3e50')
    ax[0].set_ylabel('Count', fontsize=12, color='#34495e')
    ax[0].grid(True, alpha=0.3, linestyle='--')
    ax[0].set_facecolor('#f8f9fa')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax[0].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                  f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    # Performance scores pie chart
    scores_raw = [precision, recall, f1_score]
    scores = [s for s in scores_raw if isinstance(s, (int, float)) and not math.isnan(s) and s > 0]
    colors_pie = ['#667eea', '#764ba2', '#f093fb']
    
    if scores:
        labels = []
        for s, name in zip(scores_raw, ['Precision', 'Recall', 'F1-Score']):
            if isinstance(s, (int, float)) and not math.isnan(s) and s > 0:
                labels.append(f'{name}: {s:.2%}')
        
        wedges, texts, autotexts = ax[1].pie(scores, labels=labels, autopct='%1.1f%%', startangle=90,
                                            colors=colors_pie[:len(scores)], explode=[0.05] * len(scores))
        ax[1].set_title('Performance Scores', fontsize=14, fontweight='bold', color='#2c3e50')
        
        # Enhance text styling
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
    else:
        ax[1].axis('off')
        ax[1].text(0.5, 0.5, 'No score data', ha='center', va='center', fontsize=12, color='#2c3e50')
    
    fig.patch.set_facecolor('#f8f9fa')
    st.pyplot(fig)

def show_download_options(deidentified_data, metrics, pii_detection_summary):
    """Display download options for results"""
    st.markdown("### Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate & Download CSV", use_container_width=True):
            with st.spinner("Generating CSV file..."):
                deidentified_csv = f"Deidentified_Data_{st.session_state.username}_{int(time.time())}.csv"
                deidentified_data.to_csv(deidentified_csv, index=False)
                
                # Save record
                save_deidentified_data(st.session_state.username, deidentified_csv, deidentified_csv)
                
                st.success("De-identified CSV generated successfully!")
                with open(deidentified_csv, "rb") as f:
                    st.download_button("Download De-identified CSV", f, file_name="Deidentified_Data.csv", mime="text/csv", use_container_width=True)
    
    with col2:
        if st.button("Generate & Download Accuracy Report", use_container_width=True):
            with st.spinner("Generating accuracy report..."):
                try:
                    accuracy_report_pdf = generate_accuracy_report_pdf(metrics, pii_detection_summary, st.session_state.username)
                    st.success("Accuracy report generated successfully!")
                    with open(accuracy_report_pdf, "rb") as f:
                        st.download_button("Download Accuracy Report", f, file_name="Accuracy_Report.pdf", mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.error(f"Error generating accuracy report: {str(e)}")

def show_pii_summary(pii_detection_summary):
    """Display PII detection summary"""
    if pii_detection_summary:
        st.markdown("### PII Detection Summary")
        
        total_detections = sum(pii_detection_summary.values())
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total PII Detections", total_detections)
        with col2:
            st.metric("Columns with PII", len(pii_detection_summary))
        with col3:
            avg_detections = total_detections / len(pii_detection_summary) if pii_detection_summary else 0
            st.metric("Avg per Column", f"{avg_detections:.1f}")
        
        # PII Detection by Column
        st.markdown("### PII Detection by Column")
        summary_df = pd.DataFrame.from_dict(pii_detection_summary, orient='index', columns=['Count'])
        summary_df = summary_df.sort_values('Count', ascending=False)
        st.dataframe(summary_df, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7']
            bars = ax.bar(summary_df.index, summary_df['Count'], color=colors[:len(summary_df)])
            ax.set_title("PII Detections by Column", fontsize=16, fontweight='bold', color='#2c3e50')
            ax.set_ylabel("Count", fontsize=14, color='#34495e')
            ax.set_xlabel("Columns", fontsize=14, color='#34495e')
            plt.xticks(rotation=45, ha='right', fontsize=12)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=11)
            
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.set_facecolor('#f8f9fa')
            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            fig2, ax2 = plt.subplots(figsize=(8, 8))
            colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#38f9d7']
            wedges, texts, autotexts = ax2.pie(summary_df['Count'], labels=summary_df.index, 
                                              autopct='%1.1f%%', colors=colors[:len(summary_df)], startangle=90,
                                              explode=[0.05] * len(summary_df))
            ax2.set_title("PII Distribution by Column", fontsize=16, fontweight='bold', color='#2c3e50')
            
            # Enhance text styling
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(11)
            
            fig2.patch.set_facecolor('#f8f9fa')
            plt.tight_layout()
            st.pyplot(fig2, use_container_width=True)
    else:
        st.info("No PII detected in the uploaded data. Your data appears to be clean!")

def main():
    """Main application entry point"""
    # Initialize session state for authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'session_token' not in st.session_state:
        st.session_state.session_token = None
    
    # Initialize database
    init_db()
    
    # Check for existing session token in URL parameters
    query_params = st.query_params
    if 'session_token' in query_params and 'username' in query_params:
        session_token = query_params['session_token']
        username = query_params['username']
        
        # Verify the session token
        if session_token and username and verify_session(session_token, username):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.session_token = session_token
            # Clear URL parameters to avoid showing them
            st.query_params.clear()
            st.rerun()
        else:
            # Invalid session, clear URL parameters
            st.query_params.clear()
            st.rerun()
    
    if not st.session_state.logged_in:
        show_login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
