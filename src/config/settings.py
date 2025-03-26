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
    """Get CSS styles for the application"""
    return """
        <style>
            /* Info Cards */
            .info-card {
                background-color: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 0.75rem;
                margin-bottom: 0.5rem;
                min-height: 65px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                transition: all 0.3s ease;
            }
            
            .info-card:hover {
                background-color: rgba(30, 41, 59, 0.7);
                transform: translateY(-2px);
            }
            
            .info-label {
                font-size: 0.8rem;
                font-weight: 500;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 0.25rem;
            }
            
            .info-value {
                font-size: 1.25rem;
                font-weight: 700;
                letter-spacing: -0.025em;
            }
            
            .price-value { color: #3b82f6; }
            .change-value-up { color: #22c55e; }
            .change-value-down { color: #ef4444; }
            .volume-value { color: #f59e0b; }
            .market-cap-value { color: #8b5cf6; }
            
            /* Right Sidebar */
            .right-sidebar {
                background-color: rgba(30, 41, 59, 0.5);
                border: 1px solid rgba(148, 163, 184, 0.2);
                border-radius: 8px;
                padding: 1rem;
            }
            
            .right-sidebar h3 {
                font-size: 1.1rem;
                font-weight: 600;
                color: #e2e8f0;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid rgba(148, 163, 184, 0.2);
            }
            
            .right-sidebar h4 {
                font-size: 0.9rem;
                font-weight: 500;
                color: #94a3b8;
                margin: 0.5rem 0;
            }
            
            .level-list {
                list-style: none;
                padding: 0;
                margin: 0 0 1rem 0;
            }
            
            .level-list li {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 0.25rem 0;
                font-size: 0.9rem;
            }
            
            .resistance-level {
                color: #ef4444;
                font-weight: 600;
            }
            
            .support-level {
                color: #22c55e;
                font-weight: 600;
            }
            
            .level-strength {
                color: #94a3b8;
                font-size: 0.8rem;
            }
            
            /* Hide Streamlit Components */
            #MainMenu, header, footer {display: none;}
            .stDeployButton {display: none;}
            .appview-container .main .block-container {
                padding-top: 1rem;
                padding-bottom: 1rem;
            }
        </style>
    """ 