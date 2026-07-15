import os
import re
import pandas as pd
from sqlalchemy import text
from .connection import engine, SessionLocal, Base

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sql")

def ensure_db_initialized():
    """Defensively ensures tables exist and are seeded before query execution."""
    try:
        from database import models
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        if db.query(models.Office).count() == 0:
            from utils.seeder import seed_database
            seed_database()
        db.close()
    except Exception:
        pass


def load_sql_query(query_name: str) -> str:
    """Loads a raw SQL query from the sql/ folder by name (e.g. 'global_summary')."""
    filename = f"{query_name}.sql" if not query_name.endswith(".sql") else query_name
    filepath = os.path.join(SQL_DIR, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"SQL file not found at: {filepath}")
        
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def translate_mysql_to_sqlite(sql: str) -> str:
    """
    Translates basic MySQL functions to SQLite syntax to enable local testing
    without code modification.
    """
    # 1. Translate HOUR(col) -> CAST(strftime('%H', col) AS INTEGER)
    sql = re.sub(r"\bHOUR\(([^)]+)\)", r"CAST(strftime('%H', \1) AS INTEGER)", sql)
    
    # 2. Translate DATE(col) -> strftime('%Y-%m-%d', col)
    sql = re.sub(r"\bDATE\(([^)]+)\)", r"strftime('%Y-%m-%d', \1)", sql)
    
    # 3. Translate TIMESTAMPDIFF(MINUTE, start, end) -> (strftime('%s', end) - strftime('%s', start)) / 60
    # Matches TIMESTAMPDIFF(MINUTE, <col1>, <col2>) case-insensitively
    pattern = r"TIMESTAMPDIFF\(\s*MINUTE\s*,\s*([^,]+)\s*,\s*([^)]+)\)"
    sql = re.sub(pattern, r"(strftime('%s', \2) - strftime('%s', \1)) / 60", sql, flags=re.IGNORECASE)
    
    return sql

def execute_query_to_df(query_name: str, params: dict = None) -> pd.DataFrame:
    """
    Loads, translates (if necessary), and executes a query, returning a Pandas DataFrame.
    """
    ensure_db_initialized()
    if params is None:
        params = {}
        
    # Standardize dictionary keys for SQL parameters
    # Replace None values with None so SQLAlchemy handles them as NULL
    sanitized_params = {}
    for k, v in params.items():
        sanitized_params[k] = v
        
    raw_sql = load_sql_query(query_name)
    
    # Check dialect
    dialect = engine.url.drivername
    if "sqlite" in dialect:
        sql_to_run = translate_mysql_to_sqlite(raw_sql)
    else:
        sql_to_run = raw_sql
        
    # Execute query
    with engine.connect() as conn:
        result = conn.execute(text(sql_to_run), sanitized_params)
        columns = result.keys()
        data = result.fetchall()
        
    return pd.DataFrame(data, columns=columns)
