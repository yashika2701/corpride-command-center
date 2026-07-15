import streamlit as st

def inject_premium_style():
    """
    Injects custom CSS to apply professional typography (Inter),
    sleek metric cards, glassmorphic effects, and styled headers.
    """
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <style>
            /* Apply custom typography */
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Inter', sans-serif;
            }
            
            /* Glassmorphism Metric Card Container */
            .metric-card-container {
                display: flex;
                flex-direction: column;
                padding: 20px;
                border-radius: 12px;
                background: var(--secondary-background-color, rgba(255, 255, 255, 0.05));
                border: 1px solid rgba(128, 128, 128, 0.15);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, border-color 0.2s ease;
                margin-bottom: 15px;
            }
            
            .metric-card-container:hover {
                transform: translateY(-2px);
                border-color: rgba(59, 130, 246, 0.4);
            }
            
            /* Status Accents */
            .accent-blue { border-left: 4px solid #3B82F6; }
            .accent-teal { border-left: 4px solid #0D9488; }
            .accent-amber { border-left: 4px solid #D97706; }
            .accent-red { border-left: 4px solid #E11D48; }
            .accent-green { border-left: 4px solid #10B981; }
            
            .metric-label {
                font-size: 11px;
                font-weight: 600;
                color: var(--text-color);
                opacity: 0.6;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-bottom: 5px;
            }
            
            .metric-value {
                font-size: 32px;
                font-weight: 700;
                color: var(--text-color);
                margin-bottom: 3px;
            }
            
            .metric-desc {
                font-size: 11px;
                color: var(--text-color);
                opacity: 0.5;
            }
            
            /* Question banner style */
            .question-banner {
                background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(13, 148, 136, 0.05));
                border-radius: 8px;
                padding: 12px 18px;
                border-left: 3px solid #3B82F6;
                margin-bottom: 25px;
                color: #E5E7EB;
                font-size: 14px;
                font-style: italic;
            }
            
            /* Section title style */
            .section-header {
                font-size: 20px;
                font-weight: 600;
                color: #F3F4F6;
                margin-top: 25px;
                margin-bottom: 15px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                padding-bottom: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def render_metric_card(label: str, value: str, desc: str = "", accent_color: str = "blue"):
    """
    Renders a premium HTML/CSS-styled metric card with inline styles to prevent CSS caching.
    accent_color choices: 'blue', 'teal', 'amber', 'red', 'green'
    """
    accent_class = f"accent-{accent_color}"
    st.markdown(
        f"""
        <div class="metric-card-container {accent_class}">
            <div class="metric-label" style="color: var(--text-color, #374151); opacity: 0.7; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px;">
                {label}
            </div>
            <div class="metric-value" style="color: var(--text-color, #111827); font-size: 32px; font-weight: 700; margin-bottom: 3px;">
                {value}
            </div>
            <div class="metric-desc" style="color: var(--text-color, #6B7280); opacity: 0.6; font-size: 11px;">
                {desc}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_business_question(question_text: str):
    """Renders a styled card showing the key business question answered by the page."""
    st.markdown(
        f"""
        <div class="question-banner">
            🎯 <strong>Core Business Question:</strong> "{question_text}"
        </div>
        """,
        unsafe_allow_html=True
    )
