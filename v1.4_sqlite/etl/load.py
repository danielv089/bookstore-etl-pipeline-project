import os
import pandas as pd 
import sqlite3
from etl.logger import get_logger

logger = get_logger(__name__)

def load(books_df, genre_df, in_stock_df):
    """
    Loads the given DataFrames into a SQLite database named 'books.db'.

    This function:
    - Connects to the SQLite database
    - Saves three tables: books, genres, and in_stock
    - Replaces the tables if they already exist

    Args:
        books_df (pd.DataFrame): DataFrame containing book details.
        genre_df (pd.DataFrame): DataFrame containing genre lookup values.
        in_stock_df (pd.DataFrame): DataFrame containing book stock counts.
    """
    try:
        os.makedirs('data/4_database', exist_ok=True)
        conn = sqlite3.connect('data/4_database/books.db')
        books_df.to_sql('books', conn, if_exists='replace', index=False)
        genre_df.to_sql('genres', conn, if_exists='replace', index=False)
        in_stock_df.to_sql('in_stock', conn, if_exists='replace', index=False)
    except Exception as e:
        logger.error(f"Error loading data: {e}")
    finally:
        conn.close()