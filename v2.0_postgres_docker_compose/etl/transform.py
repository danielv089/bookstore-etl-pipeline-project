import os

import pandas as pd

from etl.logger import get_logger

logger = get_logger(__name__)

def transform(books_raw_df):
    """
    Cleans and transforms the raw books DataFrame.

    This function:
    - Drops duplicates and nulls
    - Converts data types
    - Maps string ratings to numeric
    - Strips currency symbols and converts prices to float
    - Extracts stock numbers from text
    - Saves cleaned data to 'books_cleaned_data.csv'

    Args:
        books_raw_df (pd.DataFrame): Raw DataFrame with book data.

    Returns:
        pd.DataFrame: Cleaned and transformed DataFrame.
    """
    try:
        check_duplicates=books_raw_df.duplicated().sum()
        if check_duplicates !=0:
            books_raw_df=books_raw_df.drop_duplicates()
    except Exception as e:
        logger.error(f"Error dropping nulls: {e}")

    try:
        check_null=books_raw_df.isnull().sum().sum()
        if check_null!=0:
            books_raw_df=books_raw_df.dropna()
    except Exception as e:
        logger.error(f"Error dropping duplicates: {e}")

    try:
        books_raw_df['titles']=books_raw_df['titles'].astype(str)
        books_raw_df['genre']=books_raw_df['genre'].astype(str)
        books_raw_df['genre']= books_raw_df['genre'].replace(['Default', 'Add a comment'], 'Uncategorized')
        books_raw_df['ratings']=books_raw_df['ratings'].astype(str)
        rating_map = {'One': 1,'Two': 2,'Three': 3,'Four': 4,'Five': 5}
        books_raw_df['ratings']=books_raw_df['ratings'].map(rating_map)
        books_raw_df['upc']=books_raw_df['upc'].astype(str)
        books_raw_df['product_type']=books_raw_df['product_type'].astype(str)
        books_raw_df['price_excl_tax_gbp'] = books_raw_df['price_excl_tax_gbp'].astype(str).str[2:].astype(float)
        books_raw_df['price_incl_tax_gbp'] = books_raw_df['price_incl_tax_gbp'].astype(str).str[2:].astype(float)
        books_raw_df['tax'] = books_raw_df['tax'].str[2:].astype(float)
        books_raw_df['in_stock']=books_raw_df['in_stock'].str.extract(r'(\d+)').astype(int)
        books_raw_df['num_reviews']=books_raw_df['num_reviews'].astype(int)
    except Exception as e:
        logger.error(f"Error transforming column: {e}")

    try:
        os.makedirs('data/2_transform_data', exist_ok=True)
        books_raw_df.to_csv('data/2_transform_data/books_cleaned_data.csv')
    except Exception as e:
        logger.error(f"Error saving transformed data: {e}")
    
    return books_raw_df