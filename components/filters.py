import streamlit as st
from datetime import datetime, timedelta
from database.query_runner import execute_query_to_df

def render_global_sidebar_filters() -> dict:
    """
    Renders the global filter panel in the Streamlit sidebar.
    Returns a dictionary of parameters for SQL queries.
    """
    st.sidebar.markdown('<p style="font-size:18px; font-weight:bold; margin-bottom:15px; color:#3B82F6;">🔍 Global Filters</p>', unsafe_allow_html=True)
    
    # 1. Date Range Filter
    # Default to last 30 days of available data
    # (Since seeder generates 30 days of history, we buffer start_date slightly to cover all logs)
    default_start = datetime.now().date() - timedelta(days=32)
    default_end = datetime.now().date() + timedelta(days=1)
    
    date_range = st.sidebar.date_input(
        "Date Range",
        value=(default_start, default_end),
        help="Select the operational window to analyze."
    )
    
    # Handle range selection safety
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = default_start
        end_date = default_end
        
    # Format dates as strings for database SQL parameters
    start_str = f"{start_date} 00:00:00"
    end_str = f"{end_date} 23:59:59"
    
    # 2. Office Filter (Dynamically loaded)
    try:
        df_offices = execute_query_to_df("get_offices")
        office_options = ["All Offices"] + df_offices["name"].tolist()
        office_mapping = dict(zip(df_offices["name"], df_offices["id"]))
    except Exception:
        office_options = ["All Offices"]
        office_mapping = {}
        
    selected_office = st.sidebar.selectbox("Office Location", office_options)
    office_id = office_mapping.get(selected_office) if selected_office != "All Offices" else None
    
    # 3. Department Filter (Dynamically loaded)
    try:
        df_depts = execute_query_to_df("get_departments")
        dept_options = ["All Departments"] + df_depts["name"].tolist()
        dept_mapping = dict(zip(df_depts["name"], df_depts["id"]))
    except Exception:
        dept_options = ["All Departments"]
        dept_mapping = {}
        
    selected_dept = st.sidebar.selectbox("Department", dept_options)
    dept_id = dept_mapping.get(selected_dept) if selected_dept != "All Departments" else None
    
    # 4. Route Filter (Dynamically loaded)
    try:
        df_routes = execute_query_to_df("get_routes")
        route_options = ["All Routes"] + df_routes["name"].tolist()
        route_mapping = dict(zip(df_routes["name"], df_routes["id"]))
    except Exception:
        route_options = ["All Routes"]
        route_mapping = {}
        
    selected_route = st.sidebar.selectbox("Route", route_options)
    route_id = route_mapping.get(selected_route) if selected_route != "All Routes" else None
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<div style="text-align: center; color: #6B7280; font-size: 11px;">CorpRide Command Center v1.0</div>', 
        unsafe_allow_html=True
    )
    
    return {
        "start_date": start_str,
        "end_date": end_str,
        "office_id": office_id,
        "department_id": dept_id,
        "route_id": route_id
    }
