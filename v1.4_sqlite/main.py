# -----------------------------------------------------------------------------
# Script Name:        main.py
# Author:             Dániel Varga
# Created:            2025-06-21
# Last Modified:      2025-06-28
# Version:            1.4
# Description:        Main entry point for the ETL pipeline that scrapes book data
#                     from 'Books to Scrape', transforms and normalizes it, and
#                     loads it into a SQLite database.
# Website:            https://books.toscrape.com/
# -----------------------------------------------------------------------------

from etl.extract import extract
from etl.transform import transform
from etl.normalize import normalize
from etl.load import load
from etl.logger import get_logger

logger = get_logger(__name__)

def main():
    """
    Main script to run the full ETL pipeline for the books dataset.

    This script performs the following steps:
    1. Extraction
    2. Cleaning and transformation
    3. Normalization
    4. Loading to database
    Usage:
    python3 main.py
    """
    try:
        logger.info('Starting the ETL pipeline...')
        logger.info('Extracting data from source...')
        raw_data = extract()  
        logger.info('Data extracted successfully.')    

        logger.info('Cleaning and transforming the data...')
        transforming_data = transform(raw_data)  
        logger.info('Splitting data into normalized tables: books, genres, in_stock') 
        books_df, genre_df, in_stock_df = normalize(transforming_data)
        logger.info('Data cleaned and transformed successfully.') 

        logger.info('Loading data into SQLite database...')
        load(books_df,genre_df,in_stock_df)
        logger.info('All data successfully loaded into the database.')
    except Exception as e:
        logger.error(f"ETL pipeline failed: {e}")  


if __name__ == '__main__':
    main()