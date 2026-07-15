import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger("corpride.database")

# Setup declarative base
Base = declarative_base()

# Retrieve database configuration from environment variables
# If no specific MySQL URL is provided, try constructing from parts, or fallback to sqlite
DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "corpride_db")

# Allow full URL override
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Check if we should use MySQL or SQLite
    USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"
    if USE_SQLITE or (not DB_PASSWORD and DB_HOST == "localhost" and os.getenv("MYSQL_USER") is None):
        DATABASE_URL = "sqlite:///corpride.db"
        logger.info("Using SQLite fallback database: corpride.db")
    else:
        # Construct MySQL connection URL using PyMySQL driver
        DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        logger.info(f"Using MySQL database connection at {DB_HOST}:{DB_PORT}")

# Create engine
# If using sqlite, check_same_thread is needed for multi-threaded Streamlit access
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Failed to create database engine for URL: {DATABASE_URL}. Error: {e}")
    raise e

def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
