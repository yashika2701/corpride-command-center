import streamlit as st
import pandas as pd
import plotly.express as px
from components.common import inject_premium_style, render_metric_card, render_business_question
from components.filters import render_global_sidebar_filters
from database.query_runner import execute_query_to_df

# 1. Config page
st.set_page_config(page_title="Finance Dashboard - CorpRide", page_icon="💳", layout="wide")

# 2. Inject styles
inject_premium_style()

# 3. Sidebar Filters
params = render_global_sidebar_filters()

# 4. Header
st.title("💳 Finance & Audit Dashboard")
render_business_question("Are we being overcharged by vendors? Where is the billing leakage?")

# 5. Load and Execute SQL Queries
try:
    df_summary = execute_query_to_df("global_summary", params)
    df_leakage = execute_query_to_df("billing_leakage", params)
    df_dept_costs = execute_query_to_df("department_costs", params)
    
    if not df_summary.empty:
        summary = df_summary.iloc[0]
        
        # Calculate Finance Specific Metrics
        total_billed = summary['total_cost']
        total_leakage = df_leakage["invoice_amount"].sum() if not df_leakage.empty else 0.0
        clean_audited_cost = max(0.0, total_billed - total_leakage)
        anomaly_count = len(df_leakage)
        
        # Render Metrics Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card(
                "Total Billed Amount", 
                f"${total_billed:,.2f}", 
                "All vendor invoices received", 
                "blue"
            )
        with c2:
            render_metric_card(
                "Ghost Billing Leakage", 
                f"${total_leakage:,.2f}", 
                f"Flagged leakage from {anomaly_count} audits", 
                "red" if total_leakage > 0 else "green"
            )
        with c3:
            render_metric_card(
                "Clean Audited Cost", 
                f"${clean_audited_cost:,.2f}", 
                "Actual transport value delivered", 
                "teal"
            )
        with c4:
            leakage_pct = (total_leakage / total_billed * 100.0) if total_billed > 0 else 0.0
            render_metric_card(
                "Billing Leakage %", 
                f"{leakage_pct:.1f}%", 
                "Capital waste percentage (target: 0%)", 
                "red" if leakage_pct > 2.0 else "green"
            )
            
        # Visualizations Section
        st.markdown('<div class="section-header">💸 Cost Distribution & Leakage Categories</div>', unsafe_allow_html=True)
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("Department-wise Cost Allocation")
            if not df_dept_costs.empty:
                fig_dept = px.pie(
                    df_dept_costs,
                    values="total_cost",
                    names="department_name",
                    hole=0.4,
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Safe
                )
                fig_dept.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_dept, use_container_width=True)
            else:
                st.info("No department cost data found.")
                
        with col_right:
            st.subheader("Billing Waste by Anomaly Type")
            if not df_leakage.empty:
                df_leak_sum = df_leakage.groupby("anomaly_type")["invoice_amount"].sum().reset_index()
                
                fig_waste = px.bar(
                    df_leak_sum,
                    x="anomaly_type",
                    y="invoice_amount",
                    labels={"anomaly_type": "Anomaly Type", "invoice_amount": "Wasted Amount ($)"},
                    template="plotly_dark",
                    color="anomaly_type",
                    color_discrete_sequence=["#E11D48", "#F59E0B"]
                )
                fig_waste.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
                st.plotly_chart(fig_waste, use_container_width=True)
            else:
                st.info("No billing anomalies found in this filter window.")
                
        # Detailed Billing Audit Grid
        st.markdown('<div class="section-header">🔍 In-depth Billing Audit Queue</div>', unsafe_allow_html=True)
        if not df_leakage.empty:
            # Clean up grid columns
            display_df = df_leakage.rename(columns={
                "booking_id": "Booking ID",
                "employee_name": "Employee Name",
                "department_name": "Department",
                "invoice_number": "Invoice Number",
                "invoice_amount": "Amount ($)",
                "booking_status": "Booking Status",
                "ride_log_status": "GPS Log Status",
                "anomaly_type": "Audit Violation Flag",
                "scheduled_time": "Scheduled Time"
            })
            
            st.dataframe(
                display_df[["Booking ID", "Invoice Number", "Amount ($)", "Employee Name", "Department", "Booking Status", "GPS Log Status", "Audit Violation Flag", "Scheduled Time"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ Clean Audit: No duplicate billing or ghost rides detected in this period.")
            
    else:
        st.warning("⚠️ No data matches the selected filters.")
        
except Exception as e:
    st.error(f"❌ Error executing finance dashboard queries. Ensure database is running and seeded. Detail: {e}")
