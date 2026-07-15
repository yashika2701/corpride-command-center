import streamlit as st
from components.common import inject_premium_style, render_metric_card
from database.query_runner import execute_query_to_df

# 1. Config page
st.set_page_config(
    page_title="CorpRide Command Center",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Styles
inject_premium_style()

# 3. Main Header
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #1E3A8A, #0D9488); padding: 30px; border-radius: 15px; margin-bottom: 30px;">
        <h1 style="color: white; margin: 0; font-size: 38px; font-weight: 800; letter-spacing: -0.025em;">🚘 CorpRide Command Center</h1>
        <p style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 16px; font-weight: 400; opacity: 0.9;">
            Enterprise Mobility Operations Analytics Platform
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    Welcome to the **CorpRide Command Center**, a centralized decision-support platform designed to monitor 
    corporate transit performance. The application consolidates bookings, driver logs, GPS tracks, safety incidents, 
    and invoices to extract actionable operational insights.
    """
)

# 4. Portal Overview Section
st.markdown('<div class="section-header">👥 Persona-Based Dashboards</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top:0; color:#3B82F6;">📊 Executive Leadership</h3>
            <p style="font-size: 13px; color:#9CA3AF; min-height:60px;">
                Designed for high-level executives tracking overall capital efficiency, transportation sustainability, 
                and fleet utilization trends.
            </p>
            <div style="font-size:12px; font-style:italic; border-left:2px solid #3B82F6; padding-left:10px; color:#E5E7EB; margin-bottom:15px;">
                "How is fleet efficiency trending? What is the average cost per ride?"
            </div>
            <a href="/Executive_Dashboard" target="_self" style="text-decoration:none;">
                <button style="background:#3B82F6; color:white; border:none; padding:8px 16px; border-radius:5px; font-weight:600; cursor:pointer;">
                    Go to Executive View →
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top:0; color:#D97706;">💳 Finance & Audit</h3>
            <p style="font-size: 13px; color:#9CA3AF; min-height:60px;">
                Optimized for auditing billing discrepancies, identifying duplicate invoicing, and monitoring transport waste leakage.
            </p>
            <div style="font-size:12px; font-style:italic; border-left:2px solid #D97706; padding-left:10px; color:#E5E7EB; margin-bottom:15px;">
                "Are we being overcharged by vendors? Where are our cost leakages?"
            </div>
            <a href="/Finance_Dashboard" target="_self" style="text-decoration:none;">
                <button style="background:#D97706; color:white; border:none; padding:8px 16px; border-radius:5px; font-weight:600; cursor:pointer;">
                    Go to Finance View →
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top:0; color:#0D9488;">⚙️ Operations Control</h3>
            <p style="font-size: 13px; color:#9CA3AF; min-height:60px;">
                Tailored for dispatch coordinators monitoring route occupancy, scheduled SLA breaches, and driver punctuality.
            </p>
            <div style="font-size:12px; font-style:italic; border-left:2px solid #0D9488; padding-left:10px; color:#E5E7EB; margin-bottom:15px;">
                "Which routes have SLA breaches? How are delays trending during peaks?"
            </div>
            <a href="/Operations_Dashboard" target="_self" style="text-decoration:none;">
                <button style="background:#0D9488; color:white; border:none; padding:8px 16px; border-radius:5px; font-weight:600; cursor:pointer;">
                    Go to Operations View →
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="margin-top:0; color:#E11D48;">🛡️ HR & Safety</h3>
            <p style="font-size: 13px; color:#9CA3AF; min-height:60px;">
                Built to enforce employee duty of care, audit route deviation alerts, track active SOS panics, and measure resolution SLA.
            </p>
            <div style="font-size:12px; font-style:italic; border-left:2px solid #E11D48; padding-left:10px; color:#E5E7EB; margin-bottom:15px;">
                "Are there unresolved safety alerts? What is our SOS incident response time?"
            </div>
            <a href="/HR_Safety_Dashboard" target="_self" style="text-decoration:none;">
                <button style="background:#E11D48; color:white; border:none; padding:8px 16px; border-radius:5px; font-weight:600; cursor:pointer;">
                    Go to Safety View →
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# 5. Database Statistics Summary (System Health)
st.markdown('<div class="section-header">⚙️ System Health & Data Engine Status</div>', unsafe_allow_html=True)

try:
    df_stats = execute_query_to_df("db_statistics")
    if not df_stats.empty:
        stats = df_stats.iloc[0]
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Registered Employees", f"{stats['employee_count']}", "Active corporate users", "blue")
        with c2:
            render_metric_card("Active Vehicles", f"{stats['vehicle_count']}", "Corporate shuttle fleet", "teal")
        with c3:
            render_metric_card("Total Logs Processed", f"{stats['ride_count']}", "Completed rides audited", "amber")
        with c4:
            render_metric_card("SOS & Safety Alerts", f"{stats['incident_count']}", "Safety cases tracked", "red")
            
        st.success("✅ Database connection active. Operating in Analytics-First SQL Mode.")
    else:
        st.warning("⚠️ Connected to database, but statistics are empty. Run seeder.")
except Exception as e:
    st.error(f"❌ Database connection failed. Please ensure the database is seeded and database settings are correct. Error: {e}")

# Sidebar instructions
st.sidebar.title("Navigation")
st.sidebar.info("Select a dashboard from the list above to view specific stakeholder analytics.")
