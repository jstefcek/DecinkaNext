import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from django.conf import settings
from contextlib import contextmanager
from typing import Any, Dict, List

# Configure logging
log = logging.getLogger("db_manager")

# SQLAlchemy engine initialization
engine = create_engine(
    settings.DATABASE_CUSTOM_URL,
    pool_size=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

class DatabaseManager:
    """
    Manage database connections and basic operations using SQLAlchemy.
    """
    def __init__(self):
        self.engine = engine

    @contextmanager
    def get_db_connection(self):
        """Context manager for database connections"""
        try:
            connection = self.engine.connect()
            log.info("Database connection established")
            yield connection
        except SQLAlchemyError as e:
            log.error(f"Database connection error: {e}", exc_info=True)
            raise
        finally:
            if connection:
                connection.close()

    # ------------------------------------------------------------------------
    # Universal CRUD Operations
    # ------------------------------------------------------------------------
    def fetch_all(self, query_str: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Returns a list of dictionaries for all rows matching the query"""
        with self.get_db_connection() as conn:
            result = conn.execute(text(query_str), params or {})
            log.info(f"Executed query: \n{query_str} \nwith params: {params}. \nFetched rows count: {result.rowcount}")
            return [dict(row) for row in result.mappings()]

    def fetch_one(self, query_str: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Returns a dictionary for the first row matching the query or None if no rows match"""
        with self.get_db_connection() as conn:
            result = conn.execute(text(query_str), params or {})
            row = result.mappings().first()
            log.info(f"Executed query: \n{query_str} \nwith params: {params}. \nFetched row: {row}")
            return dict(row) if row else None

    def execute(self, query_str: str, params: Dict[str, Any] = None) -> int:
        """For INSERT, UPDATE, DELETE. Returns the number of affected rows"""
        with self.get_db_connection() as conn:
            result = conn.execute(text(query_str), params or {})
            conn.commit()
            log.info(f"Executed query: \n{query_str} \nwith params: {params}. \nRows affected: {result.rowcount}")
            return result.rowcount

    def insert_get_id(self, query_str: str, params: Dict[str, Any] = None) -> int:
        """For INSERT, where you need to return the ID of the new row immediately"""
        with self.get_db_connection() as conn:
            result = conn.execute(text(query_str), params or {})
            conn.commit()
            log.info(f"Executed insert query: \n{query_str} \nwith params: {params}. \nNew row ID: {result.lastrowid}")
            return result.lastrowid
        
# Initialize a global instance of DatabaseManager to be used across the application
db_engine = DatabaseManager()

try:
    log.info("Testing DB connection...")
    db_engine.fetch_all("SELECT 1")
    log.info("Connection successful!")
except Exception as e:
    log.error(f"Connection failed: {e}")