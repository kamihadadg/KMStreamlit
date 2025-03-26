import streamlit as st

def setup_page_config():
    """Setup page configuration"""
    st.set_page_config(
        layout="wide",
        page_title="Crypto Chart Pro",
        page_icon="📈",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': None
        }
    )

def get_styles():
    return """
        <style>
            /* Hide Streamlit elements */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Main block container */
            .block-container {
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
            }
            
            /* Info cards container */
            .info-cards-container {
                padding: 0.5rem;
                margin-top: 0;
                display: flex;
                gap: 0.5rem;
            }
            
            /* Info cards */
            .info-card {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 0.5rem;
                padding: 0.75rem;
                margin: 0;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                text-align: center;
                min-height: 65px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                transition: transform 0.2s;
                flex: 1;
            }
            
            .info-card:hover {
                transform: translateY(-2px);
            }
            
            .info-label {
                color: #94a3b8;
                font-size: 0.8rem;
                font-weight: 500;
                margin-bottom: 0.25rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            
            .info-value {
                font-size: 1.25rem;
                font-weight: 700;
                letter-spacing: 0.025em;
                line-height: 1.2;
            }
            
            /* Price value colors */
            .price-value { color: #3b82f6 !important; }
            .change-value-up { color: #22c55e !important; }
            .change-value-down { color: #ef4444 !important; }
            .volume-value { color: #f59e0b !important; }
            .market-cap-value { color: #8b5cf6 !important; }
            
            /* Right sidebar styles */
            .right-sidebar {
                background-color: #1e293b;
                border-radius: 0.5rem;
                padding: 0.75rem;
                margin: 0;
            }
            
            .right-sidebar h3 {
                color: #f8fafc;
                font-size: 1rem;
                margin-bottom: 0.5rem;
                border-bottom: 1px solid #334155;
                padding-bottom: 0.25rem;
            }
            
            .right-sidebar h4 {
                color: #e2e8f0;
                font-size: 0.9rem;
                margin: 0.25rem 0;
            }
            
            .right-sidebar ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            
            .right-sidebar li {
                color: #94a3b8;
                font-size: 0.85rem;
                padding: 0.15rem 0;
                margin: 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .support-level {
                color: #22c55e;
                font-weight: 500;
            }
            
            .resistance-level {
                color: #ef4444;
                font-weight: 500;
            }
            
            .level-strength {
                color: #94a3b8;
                font-size: 0.75rem;
                margin-left: 0.5rem;
            }
            
            /* Titles */
            .stMarkdown h1 {
                color: #f8fafc;
                margin-bottom: 0.5rem;
            }
            
            .stMarkdown h2 {
                color: #f8fafc;
                margin-bottom: 0.5rem;
            }
            
            .stMarkdown h3 {
                color: #f8fafc;
                margin-bottom: 0.5rem;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #0f172a;
            }
            
            /* Main content */
            .main .block-container {
                background-color: #0f172a;
            }
            
            /* Buttons */
            .stButton button {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 0.375rem;
                padding: 0.5rem 1rem;
                font-weight: 500;
                transition: background-color 0.2s;
            }
            
            .stButton button:hover {
                background-color: #2563eb;
            }
            
            /* Checkboxes and radio buttons */
            .stCheckbox label, .stRadio label {
                color: #f8fafc;
            }
            
            /* Select boxes */
            .stSelectbox select {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 0.375rem;
            }
            
            /* Number inputs */
            .stNumberInput input {
                background-color: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 0.375rem;
            }
        </style>
    """ 