import streamlit as st
import pandas as pd
import plotly.express as px
from components.common import inject_premium_style, render_metric_card, render_business_question
from components.filters import render_global_sidebar_filters
from database.query_runner import execute_query_to_df

# 1. Config page
st.set_page_config(page_title="Safety Dashboard - CorpRide", page_icon="🛡️", layout="wide")

# 2. Inject styles
inject_premium_style()

# 3. Sidebar Filters
params = render_global_sidebar_filters()

# 4. Header
st.title("🛡️ HR & Safety Dashboard")
render_business_question("Are there unresolved SOS events? What is the safety compliance rate?")

# 5. Load and Execute SQL Queries
try:
    df_metrics = execute_query_to_df("safety_metrics", params)
    df_incidents = execute_query_to_df("safety_incidents", params)
    
    if not df_metrics.empty:
        metrics = df_metrics.iloc[0]
        
        # Calculate SOS Resolution SLA
        avg_res_time = 0.0
        if not df_incidents.empty:
            df_sos_resolved = df_incidents[(df_incidents["incident_type"] == "SOS") & (df_incidents["incident_status"] == "Resolved")]
            if not df_sos_resolved.empty:
                avg_res_time = df_sos_resolved["resolution_time_minutes"].mean()
                
        # Render Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card(
                "Active SOS Panics", 
                f"{metrics['active_sos']}", 
                "SOS alerts currently unresolved", 
                "red" if metrics['active_sos'] > 0 else "green"
            )
        with c2:
            render_metric_card(
                "SOS Resolution SLA", 
                f"{avg_res_time:.1f} mins" if avg_res_time > 0 else "N/A", 
                "Avg dispatcher close-out time", 
                "green" if avg_res_time < 30 else "amber"
            )
        with c3:
            render_metric_card(
                "Route Deviation Rate", 
                f"{metrics['route_deviation_rate']:.1f}%", 
                "Percentage of GPS route violations", 
                "teal" if metrics['route_deviation_rate'] < 5 else "amber"
            )
        with c4:
            render_metric_card(
                "Total Safety Incidents", 
                f"{metrics['total_incidents']}", 
                "SOS panic and delay alerts combined", 
                "blue"
            )
            
        st.markdown('<div class="section-header">🚨 Safety Event Breakdown & Escalation Queue</div>', unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Incident Type Distribution")
            if not df_incidents.empty:
                fig_inc = px.pie(
                    df_incidents,
                    names="incident_type",
                    template="plotly_dark",
                    color="incident_type",
                    color_discrete_map={"SOS": "#E11D48", "Delay": "#3B82F6", "Deviation": "#F59E0B", "Accident": "#9F1239"}
                )
                fig_inc.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_inc, use_container_width=True)
            else:
                st.info("No safety incident records found.")
                
        with col_right:
            st.subheader("Route Deviations by Route (GPS Violations)")
            if not df_incidents.empty:
                df_deviations = df_incidents[df_incidents["route_deviation"] == True]
                if not df_deviations.empty:
                    df_dev_grouped = df_deviations.groupby("route_name")["incident_id"].count().reset_index()
                    df_dev_grouped = df_dev_grouped.rename(columns={"incident_id": "Deviations"})
                    df_dev_grouped = df_dev_grouped.sort_values("Deviations", ascending=True)
                    
                    fig_dev = px.bar(
                        df_dev_grouped,
                        x="Deviations",
                        y="route_name",
                        orientation="h",
                        labels={"Deviations": "GPS Route Deviations (Qty)", "route_name": "Route"},
                        template="plotly_dark",
                        color_discrete_sequence=["#D97706"]
                    )
                    fig_dev.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_dev, use_container_width=True)
                else:
                    st.success("✅ Excellent: 0 GPS route deviations recorded on active trips.")
            else:
                st.info("No route deviation stats available.")
                
        # Escalation Queue (Active and resolved incidents table)
        st.markdown('<div class="section-header">🚨 Dispatch Escalation & Audit Queue</div>', unsafe_allow_html=True)
        if not df_incidents.empty:
            display_df = df_incidents.copy()
            
            # Format display dataframe
            display_df["resolution_time"] = display_df["resolution_time_minutes"].apply(
                lambda x: f"{int(x)} mins" if pd.notna(x) else "Pending Action"
            )
            display_df = display_df.rename(columns={
                "incident_type": "Incident Type",
                "severity": "Severity",
                "incident_status": "Status",
                "employee_name": "Employee Name",
                "driver_name": "Driver Name",
                "license_plate": "Vehicle Plate",
                "route_name": "Route Name",
                "created_at": "Incident Time",
                "resolution_notes": "Resolution Notes"
            })
            
            # Highlight Open SOS incidents visually by separating them or ordering them first
            # Streamlit dataframe allows custom column configs or highlight styles
            st.dataframe(
                display_df[["Incident Type", "Severity", "Status", "Employee Name", "Driver Name", "Vehicle Plate", "Route Name", "Incident Time", "resolution_time", "Resolution Notes"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ Clean Record: No security alerts or SOS triggers active.")
            
    else:
        st.warning("⚠️ No data matches the selected filters.")
        
except Exception as e:
    st.error(f"❌ Error executing safety dashboard queries. Ensure database is running and seeded. Detail: {e}")
