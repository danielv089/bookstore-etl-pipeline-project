import os

import pandas as pd

from etl.logger import get_logger

logger = get_logger(__name__)

def normalize(books_clean_df):
    """
    Normalizes the cleaned book DataFrame into separate tables for relational storage.

    This function:
    - Extracts unique genres and assigns IDs to create a genre lookup table.
    - Replaces genre names in the books table with corresponding genre IDs.
    - Creates three DataFrames:
        1. books_df: Main book details with genre_id.
        2. genre_df: Genre lookup table.
        3. in_stock_df: Availability of books (stock count).
    - Saves each DataFrame to a separate CSV file.

    Args:
        books_clean_df (pd.DataFrame): The cleaned DataFrame containing book data.

    Returns:
        tuple: A tuple of three DataFrames:
            - books_df (pd.DataFrame)
            - genre_df (pd.DataFrame)
            - in_stock_df (pd.DataFrame)
    """
    try:
        unique_genres = books_clean_df['genre'].unique()
        unique_genres=[data.strip() for data in unique_genres]
        unique_genres=sorted(unique_genres)
        genre_to_id = {genre: idx for idx, genre in enumerate(unique_genres, start=1)}
        genre_df = pd.DataFrame({'id': list(genre_to_id.values()),'genre': list(genre_to_id.keys())})
        books_clean_df['genre']=books_clean_df['genre'].map(genre_to_id)
        books_clean_df=books_clean_df.rename(columns={'genre':'genre_id'})
        books_df=books_clean_df[['upc', 'titles', 'genre_id', 'ratings', 'product_type','price_excl_tax_gbp', 'price_incl_tax_gbp', 'tax', 'num_reviews']].copy()
        in_stock_df = books_clean_df[['upc', 'in_stock']].copy()
    except Exception as e:
        logger.error(f"Error normalization: {e}")

    try:
        os.makedirs('data/3_normalized_data', exist_ok=True)
        books_df.to_csv('data/3_normalized_data/books.csv', index=False)
        genre_df.to_csv('data/3_normalized_data/genres.csv', index=False)
        in_stock_df.to_csv('data/3_normalized_data/in_stock.csv', index=False)
    except Exception as e:
        logger.error(f"Error saving normalized data: {e}")

    return books_df, genre_df, in_stock_df
