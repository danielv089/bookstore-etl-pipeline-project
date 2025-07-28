import os
import pandas as pd 
import psycopg
from etl.logger import get_logger
from psycopg.errors import DuplicateDatabase

logger = get_logger(__name__)

def load():
    """
    Creates the 'books_website' PostgreSQL database if it doesn't exist, 
    creates all tables, if they don't exist ('books', 'genres', 'in_stock'), 
    and loads data from CSV files into these tables using PostgreSQL's COPY command.

    The database connection parameters (user, password, host, port) are read 
    from environment variables with the following defaults:
        - POSTGRES_USER (default: 'postgres')
        - POSTGRES_PASSWORD (default: 'postgres')
        - POSTGRES_HOST (default: 'localhost')
        - POSTGRES_PORT (default: '5432')

    This function handles the database creation, table setup, and bulk data loading.
    """
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "postgres")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    with psycopg.connect(dbname="postgres", user=user, password=password, host=host, port=port) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            try:
                cur.execute('CREATE DATABASE books_website')
            except DuplicateDatabase:
                logger.info('Database books already exists')

    with psycopg.connect(dbname="books_website", user=user, password=password, host=host, port=port ) as conn:
        with conn.cursor() as cur:


            cur.execute('''
                CREATE TABLE IF NOT EXISTS genres (
                genre_id INTEGER 	PRIMARY KEY,
	            genre VARCHAR(50)
                )
            ''')

            cur.execute('''
               CREATE TABLE IF NOT EXISTS in_stock (
               upc CHAR(25) PRIMARY KEY,
	           in_stock INTEGER
               );
            ''')

            cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
            upc CHAR(25) REFERENCES in_stock(upc),
	        titles VARCHAR(300),
	        genre_id SMALLINT REFERENCES genres(genre_id),
	        ratings SMALLINT,
	        product_type VARCHAR(15),
	        price_excl_tax_gbp NUMERIC(5,2),
	        price_incl_tax_gbp NUMERIC(5,2),
	        tax NUMERIC(5,2),
	        num_reviews INTEGER
            )
            ''')

            cur.execute('TRUNCATE TABLE books, genres, in_stock;')
         
    with psycopg.connect(dbname="books_website", user=user, password=password, host=host, port=port) as conn:
        with conn.cursor() as cur:
            with cur.copy("COPY in_stock (upc, in_stock) FROM STDIN CSV HEADER") as copy:
                with open('data/3_normalized_data/in_stock.csv', 'r', encoding='utf-8') as f:
                    for line in f:
                        copy.write(line)

            with cur.copy("COPY genres (genre_id, genre) FROM STDIN CSV HEADER") as copy:
                with open('data/3_normalized_data/genres.csv', 'r', encoding='utf-8') as f:
                    for line in f:
                        copy.write(line)

            with cur.copy("COPY books (upc, titles, genre_id, ratings, product_type, price_excl_tax_gbp, price_incl_tax_gbp, tax, num_reviews) FROM STDIN CSV HEADER") as copy:
                with open('data/3_normalized_data/books.csv', 'r', encoding='utf-8') as f:
                    for line in f:
                        copy.write(line)
            
  



    

                






        



                