"""
Module for loading data to SQLite database.
"""
import logging
import pandas as pd
import sqlite3
from sqlalchemy import create_engine

logger = logging.getLogger(__name__)

def load_to_sqlite(df, table_name, db_uri, if_exists='replace', index=False):
    """
    Load DataFrame to SQLite database.
    
    Args:
        df (pandas.DataFrame): DataFrame to load
        table_name (str): Name of the table to create/update
        db_uri (str): SQLite database URI
        if_exists (str): How to behave if the table exists
                       - 'fail': Raise a ValueError
                       - 'replace': Drop the table before inserting new values
                       - 'append': Insert new values to the existing table
        index (bool): Write DataFrame index as a column
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Loading data to SQLite table: {table_name}")
    
    try:
        # Check if DataFrame is empty
        if df.empty:
            logger.error("Cannot load empty DataFrame to database")
            return False
        
        # Create SQLAlchemy engine
        engine = create_engine(db_uri)
        
        # Write DataFrame to SQLite
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists,
            index=index
        )
        
        # Verify the data was loaded by counting rows
        with engine.connect() as connection:
            # SQLAlchemy 2.0 requires using text() for raw SQL
            from sqlalchemy import text
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            row_count = result.scalar()
        
        logger.info(f"Successfully loaded {row_count} rows to table '{table_name}'")
        return True
    
    except Exception as e:
        logger.error(f"Error loading data to SQLite: {e}")
        return False

def create_database_schema(db_uri, tables_info):
    """
    Create database schema for COVID-19 data.
    
    Args:
        db_uri (str): SQLite database URI
        tables_info (dict): Dictionary with table names as keys and column definitions as values
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Creating database schema")
    
    try:
        # Extract database path from URI
        db_path = db_uri.replace('sqlite:///', '')
        
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create tables
        for table_name, columns in tables_info.items():
            # Build CREATE TABLE statement
            columns_str = ', '.join(columns)
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            
            # Execute CREATE TABLE
            cursor.execute(create_table_sql)
            logger.info(f"Created table: {table_name}")
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        logger.info("Database schema created successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error creating database schema: {e}")
        return False