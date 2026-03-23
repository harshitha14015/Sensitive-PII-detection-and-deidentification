"""
Common UI Styling and Components
"""
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app"""
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1f77b4;
        --secondary-color: #ff7f0e;
        --success-color: #2ca02c;
        --danger-color: #d62728;
        --warning-color: #ff7f0e;
        --info-color: #17a2b8;
        --light-color: #f8f9fa;
        --dark-color: #343a40;
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --gradient-danger: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .stApp > header {
        background: var(--gradient-primary);
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gradient-primary);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Success button */
    .stButton > button[kind="primary"] {
        background: var(--gradient-success);
    }
    
    /* Danger button */
    .stButton > button[kind="secondary"] {
        background: var(--gradient-danger);
    }
    
    /* Metric cards styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid var(--primary-color);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* TP card */
    .metric-tp {
        border-left-color: var(--success-color);
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    }
    
    /* TN card */
    .metric-tn {
        border-left-color: var(--info-color);
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
    }
    
    /* FP card */
    .metric-fp {
        border-left-color: var(--warning-color);
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    }
    
    /* FN card */
    .metric-fn {
        border-left-color: var(--danger-color);
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed var(--primary-color);
        border-radius: 15px;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
                
    .stFileUploader > div:hover {
        border-color: var(--secondary-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: var(--gradient-primary);
        border-radius: 10px;
    }
    
    /* Alert styling */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    h1 {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Subtitle styling */
    h2 {
        color: var(--primary-color);
        border-bottom: 3px solid var(--primary-color);
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }
    </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, description, card_type="default"):
    """Create a styled metric card"""
    card_class = f"metric-{card_type}" if card_type != "default" else ""
    
    return f"""
    <div class="metric-card {card_class}" style="text-align: center; padding: 0.5rem;">
        <h4 style="margin: 0; font-size: 0.9rem;">{title}</h4>
        <h3 style="margin: 0.3rem 0; font-size: 1.5rem;">{value}</h3>
        <p style="margin: 0; font-size: 0.7rem; color: #666;">{description}</p>
    </div>
    """
