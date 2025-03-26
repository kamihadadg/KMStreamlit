import streamlit as st

def setup_page_config():
    st.set_page_config(
        layout="wide",
        page_title="Crypto Chart Pro",
        page_icon="📈",
        initial_sidebar_state="expanded"
    )

def get_styles():
    return """
        <style>
        .main {
            background-color: #0f172a;
            color: #e2e8f0;
        }
        .sidebar .sidebar-content {
            background-color: #1e293b;
            color: #e2e8f0;
        }
        .stButton>button {
            background-color: #3b82f6;
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #2563eb;
            transform: translateY(-1px);
        }
        .stSelectbox, .stMultiselect, .stSlider {
            color: #e2e8f0;
        }
        .reportview-container .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            max-height: 100vh;
        }
        .css-1d391kg {
            padding-top: 1rem;
        }
        .stMarkdown {
            color: #e2e8f0;
        }
        .price-card {
            background-color: #1e293b;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .metric-card {
            background-color: #1e293b;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #3b82f6;
        }
        .metric-label {
            font-size: 0.875rem;
            color: #94a3b8;
        }
        </style>
    """ 