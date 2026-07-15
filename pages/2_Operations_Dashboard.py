import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.common import inject_premium_style, render_metric_card, render_business_question
from components.filters import render_global_sidebar_filters
from database.query_runner import execute_query_to_df

# 1. Config page
st.set_page_config(page_title="Operations Dashboard - CorpRide", page_icon="⚙️", layout="wide")

# 2. Inject styles
inject_premium_style()

# 3. Sidebar Filters
params = render_global_sidebar_filters()

# 4. Header
st.title("⚙️ Operations Control Dashboard")
render_business_question("Which routes have SLA breaches? How are delays trending?")

# 5. Load and Execute SQL Queries
try:
    df_summary = execute_query_to_df("global_summary", params)
    df_congestion = execute_query_to_df("congestion_analytics", params)
    df_routes = execute_query_to_df("route_performance", params)
    df_util = execute_query_to_df("fleet_utilization", params)
    
    if not df_summary.empty:
        summary = df_summary.iloc[0]
        
        # Calculate Operations metrics
        avg_occupancy = df_util["passenger_count"].mean() if not df_util.empty else 0.0
        
        # Render Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card(
                "Average Pickup Delay", 
                f"{summary['avg_pickup_delay']:.1f} mins", 
                "Lower is better (target: <10m)", 
                "red" if summary['avg_pickup_delay'] > 12 else "blue"
            )
        with c2:
            render_metric_card(
                "SLA Breach Rate", 
                f"{summary['sla_breach_rate']:.1f}%", 
                "Percentage of late pickups/runs", 
                "red" if summary['sla_breach_rate'] > 20 else "teal"
            )
        with c3:
            render_metric_card(
                "Ride Completion Rate", 
                f"{summary['completion_rate']:.1f}%", 
                "Completed vs. booked rides", 
                "green" if summary['completion_rate'] > 85 else "amber"
            )
        with c4:
            render_metric_card(
                "Average Occupancy", 
                f"{avg_occupancy:.1f} pax", 
                "Average passengers per vehicle", 
                "blue"
            )
            
        st.markdown('<div class="section-header">🚗 Commute Peak Congestion & Route Compliance</div>', unsafe_allow_html=True)
        
        # Visualizations Section
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Hourly Delay Trend & Booking Volumes")
            if not df_congestion.empty:
                # Build dual-axis or layered chart
                fig_congestion = go.Figure()
                
                # Bar chart for booking volumes
                fig_congestion.add_trace(
                    go.Bar(
                        x=df_congestion["hour_of_day"],
                        y=df_congestion["total_bookings"],
                        name="Bookings (Qty)",
                        marker_color="rgba(59, 130, 246, 0.4)",
                        yaxis="y"
                    )
                )
                
                # Line chart for average delay mins
                fig_congestion.add_trace(
                    go.Scatter(
                        x=df_congestion["hour_of_day"],
                        y=df_congestion["avg_pickup_delay_mins"],
                        name="Avg Delay (Mins)",
                        line=dict(color="#E11D48", width=3),
                        marker=dict(size=8),
                        yaxis="y2"
                    )
                )
                
                # Configure dual Y-axes
                fig_congestion.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title="Hour of Day (24h)", tickmode="linear", tick0=0, dtick=1),
                    yaxis=dict(title="Total Bookings", side="left"),
                    yaxis2=dict(title="Average Delay (Minutes)", side="right", overlaying="y", showgrid=False),
                    legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)")
                )
                st.plotly_chart(fig_congestion, use_container_width=True)
                
                st.caption("💡 *Note: Delays and breach rates spike severely during morning (8-10h) and evening (17-19h) commute peak windows.*")
            else:
                st.info("No hourly congestion data found.")
                
        with col_right:
            st.subheader("SLA Breach Rate by Route")
            if not df_routes.empty:
                fig_route_breach = px.bar(
                    df_routes,
                    x="route_sla_breach_rate",
                    y="route_name",
                    orientation="h",
                    labels={"route_sla_breach_rate": "SLA Breach Rate (%)", "route_name": "Route"},
                    template="plotly_dark",
                    color="route_sla_breach_rate",
                    color_continuous_scale="Reds"
                )
                fig_route_breach.update_layout(
                    xaxis_range=[0, 100], 
                    plot_bgcolor="rgba(0,0,0,0)", 
                    paper_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_route_breach, use_container_width=True)
            else:
                st.info("No route compliance data found.")
                
        # Detailed route performance grid
        st.markdown('<div class="section-header">📋 Route Performance Overview</div>', unsafe_allow_html=True)
        if not df_routes.empty:
            # Rename columns for presentation
            display_df = df_routes.rename(columns={
                "route_name": "Route Name",
                "total_bookings": "Total Bookings",
                "completed_rides": "Completed Rides",
                "completion_rate": "Completion Rate (%)",
                "avg_pickup_delay_mins": "Avg Delay (Mins)",
                "route_sla_breach_rate": "SLA Breach Rate (%)"
            })
            
            st.dataframe(
                display_df[["Route Name", "Total Bookings", "Completed Rides", "Completion Rate (%)", "Avg Delay (Mins)", "SLA Breach Rate (%)"]],
                use_container_width=True,
                hide_index=True
            )
            
    else:
        st.warning("⚠️ No data matches the selected filters.")
        
except Exception as e:
    st.error(f"❌ Error executing operations dashboard queries. Ensure database is running and seeded. Detail: {e}")
