import streamlit as st
import pandas as pd
import plotly.express as px
from components.common import inject_premium_style, render_metric_card, render_business_question
from components.filters import render_global_sidebar_filters
from database.query_runner import execute_query_to_df

# 1. Config page
st.set_page_config(page_title="Executive Dashboard - CorpRide", page_icon="📊", layout="wide")

# 2. Inject styles
inject_premium_style()

# 3. Sidebar Filters
params = render_global_sidebar_filters()

# 4. Header
st.title("📊 Executive Leadership Dashboard")
render_business_question("How is fleet efficiency trending? What is the average cost per ride?")

# 5. Load and Execute SQL Queries
try:
    df_summary = execute_query_to_df("global_summary", params)
    df_util = execute_query_to_df("fleet_utilization", params)
    
    if not df_summary.empty:
        summary = df_summary.iloc[0]
        
        # Calculate Aggregated Fleet Utilization Rate (North Star)
        avg_utilization = df_util["utilization_rate"].mean() if not df_util.empty else 0.0
        
        # Render Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card(
                "Fleet Utilization Rate", 
                f"{avg_utilization:.1f}%", 
                "North Star KPI (seating capacity used)", 
                "green" if avg_utilization > 30 else "amber"
            )
        with c2:
            render_metric_card(
                "Total Transport Cost", 
                f"${summary['total_cost']:,.2f}", 
                "Billed vendor invoices in period", 
                "blue"
            )
        with c3:
            render_metric_card(
                "Average Cost per Ride", 
                f"${summary['cost_per_ride']:.2f}", 
                "Lower is better (target: <$200)", 
                "teal"
            )
        with c4:
            render_metric_card(
                "SLA Compliance Rate", 
                f"{(100.0 - summary['sla_breach_rate']):.1f}%", 
                "Punctuality and on-time drop-offs", 
                "blue" if (100.0 - summary['sla_breach_rate']) > 80 else "red"
            )
            
        st.markdown('<div class="section-header">📈 Efficiency & Trend Analysis</div>', unsafe_allow_html=True)
        
        # Visualizations Section
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Daily Fleet Utilization Trend (North Star)")
            if not df_util.empty:
                # Group by trip_date to get daily average utilization
                df_daily_util = df_util.groupby("trip_date")["utilization_rate"].mean().reset_index()
                df_daily_util = df_daily_util.sort_values("trip_date")
                
                fig_util = px.line(
                    df_daily_util,
                    x="trip_date",
                    y="utilization_rate",
                    labels={"trip_date": "Date", "utilization_rate": "Utilization (%)"},
                    template="plotly_dark",
                    markers=True,
                    color_discrete_sequence=["#0D9488"]
                )
                fig_util.update_layout(yaxis_range=[0, 100], plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_util, use_container_width=True)
            else:
                st.info("No utilization records found for the selected filter criteria.")
                
        with col_right:
            st.subheader("Average Fleet Utilization by Route")
            if not df_util.empty:
                # Group by route_name
                df_route_util = df_util.groupby("route_name")["utilization_rate"].mean().reset_index()
                df_route_util = df_route_util.sort_values("utilization_rate", ascending=True)
                
                fig_route = px.bar(
                    df_route_util,
                    x="utilization_rate",
                    y="route_name",
                    orientation="h",
                    labels={"utilization_rate": "Utilization (%)", "route_name": "Route"},
                    template="plotly_dark",
                    color="utilization_rate",
                    color_continuous_scale="Teal"
                )
                fig_route.update_layout(
                    xaxis_range=[0, 100], 
                    plot_bgcolor="rgba(0,0,0,0)", 
                    paper_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_route, use_container_width=True)
            else:
                st.info("No route utilization data found.")
                
    else:
        st.warning("⚠️ No data matches the selected filters.")
        
except Exception as e:
    st.error(f"❌ Error executing queries. Ensure database is running and seeded. Detail: {e}")
