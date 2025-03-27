import streamlit as st

def setup_page_config():
    """Setup page configuration"""
    st.set_page_config(
        page_title="Technical Chart",
        page_icon="📈",
        layout="wide",
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

    /* Remove extra padding */
    .block-container { 
        padding-top: 1rem; 
        padding-bottom: 0; 
        max-width: 95rem; 
    }

    /* Info Cards */
    .info-card { 
        background-color: rgba(30, 41, 59, 0.5); 
        border: 1px solid rgba(148, 163, 184, 0.1); 
        border-radius: 0.5rem; 
        padding: 0.75rem; 
        min-height: 65px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
        align-items: center; 
        transition: all 0.2s ease-in-out; 
    }

    .info-card:hover { 
        border-color: rgba(148, 163, 184, 0.2); 
        transform: translateY(-2px); 
    }

    .info-label { 
        font-size: 0.8rem; 
        font-weight: 500; 
        text-transform: uppercase; 
        letter-spacing: 0.05em; 
        color: #94a3b8; 
        margin-bottom: 0.25rem; 
    }

    .info-value { 
        font-size: 1.25rem; 
        font-weight: 700; 
        letter-spacing: -0.025em; 
        line-height: 1.2; 
    }

    /* Value Colors */
    .price-value { color: #3b82f6; }
    .change-value-up { color: #22c55e; }
    .change-value-down { color: #ef4444; }
    .volume-value { color: #f59e0b; }
    .market-cap-value { color: #8b5cf6; }

    /* Right Sidebar */
    .sidebar-section { 
        background-color: rgba(30, 41, 59, 0.5); 
        border: 1px solid rgba(148, 163, 184, 0.1); 
        border-radius: 0.5rem; 
        padding: 1rem; 
        margin-bottom: 1rem; 
    }

    .sidebar-section h3 { 
        font-size: 1rem; 
        font-weight: 600; 
        color: #e2e8f0; 
        margin: 0 0 1rem 0; 
        padding-bottom: 0.5rem; 
        border-bottom: 1px solid rgba(148, 163, 184, 0.1); 
    }

    .level-section { 
        margin-bottom: 1.5rem; 
    }

    .level-section:last-child { 
        margin-bottom: 0; 
    }

    .level-section h4 { 
        font-size: 0.9rem; 
        font-weight: 500; 
        color: #94a3b8; 
        margin: 0 0 0.5rem 0; 
    }

    .level-list { 
        list-style: none; 
        padding: 0; 
        margin: 0; 
    }

    .level-item { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 0.5rem; 
        border-radius: 0.25rem; 
        margin-bottom: 0.25rem; 
        background-color: rgba(30, 41, 59, 0.5); 
    }

    .level-item:last-child { 
        margin-bottom: 0; 
    }

    .level-price { 
        font-size: 0.9rem; 
        font-weight: 600; 
    }

    .level-price.resistance { color: #ef4444; }
    .level-price.support { color: #22c55e; }
    .level-strength { 
        font-size: 0.8rem; 
        color: #94a3b8; 
    }

    /* Buttons and Form Elements */
    .stButton > button { 
        background-color: #3b82f6; 
        color: white; 
        border: none; 
        padding: 0.5rem 1rem; 
        border-radius: 0.25rem; 
        font-weight: 500; 
        transition: all 0.2s ease-in-out; 
    }

    .stButton > button:hover { 
        background-color: #2563eb; 
        transform: translateY(-1px); 
    }

    .stCheckbox > label { color: #e2e8f0; }
    .stSelectbox > div > div { 
        background-color: rgba(30, 41, 59, 0.5); 
        border: 1px solid rgba(148, 163, 184, 0.1); 
        color: #e2e8f0; 
    }
    .stNumberInput > div > div > input { 
        background-color: rgba(30, 41, 59, 0.5); 
        border: 1px solid rgba(148, 163, 184, 0.1); 
        color: #e2e8f0; 
    }
    </style>
    """ 