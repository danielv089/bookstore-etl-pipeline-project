#!/usr/bin/env python3

# -----------------------------------------------------------------------------
# Script Name:        etl_pipeline.py
# Author:             Dániel Varga
# Created:            2025-06-21
# Last Modified:      2025-06-21
# Version:            1.0
# Description:        ETL pipeline that scrapes book data from the website
#                     Books to Scrape.
#                     Then transforms and normalizes it, then loads it into SQLite.
# Website:            https://books.toscrape.com/
# -----------------------------------------------------------------------------

import pandas as pd 
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import sqlite3


def logger(message):
    """
    Logs a message to the console and appends it with a timestamp to a log file.

    The log is saved in 'pipeline_log.text' with the format:
    'YYYY-Mon-DD-HH:MM:SS : message'.

    Args:
        message (str): The log message to record.
    """
    print(message)
    timestamp_format = "%Y-%h-%d-%H:%M:%S" 
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open('pipeline_log.text',"a") as f:
        f.write(timestamp + " : " + message + "\n")


def extract():
    """
    Extracts book data from the 'Books to Scrape' website.

    Scrapes the first catalog page and retrieves metadata for each book,
    including title, genre, rating, price, stock info, UPC, and number of reviews.
    The data is returned as a pandas DataFrame and also saved to 'books_raw_data.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing raw book data.
    """
    book_dict={'titles':[], 'genre':[], 'ratings':[], 'upc':[], 'product_type':[], 'price_excl_tax_gbp':[], 'price_incl_tax_gbp':[], 'tax':[], 'in_stock':[], 'num_reviews':[]}

    for page_num in range(1,51):
        try:
            url=f'https://books.toscrape.com/catalogue/page-{page_num}.html'
            soup=BeautifulSoup(requests.get(url).text, 'html.parser')
            books=soup.find_all('h3')

        except Exception as e:
            print(f"Failed to load page {page_num}: {e}")
            continue    

        for book in books:
            try:
                a_tag=book.find('a')
                relative_link=a_tag['href']
                full_link='https://books.toscrape.com/catalogue/' + relative_link

                soup_2=BeautifulSoup(requests.get(full_link).text, 'html.parser')
                title=soup_2.find('li', class_='active').text
                breadcrumb=soup_2.find('ul', class_='breadcrumb')
                genre_li=breadcrumb.find_all('li')[2].text.strip()
                rating=soup_2.find('p', class_='star-rating')['class'][1]

                table=soup_2.find('table', class_='table table-striped')
                product_info = {}
                for row in table.find_all('tr'):
                    key = row.th.text.strip()
                    value = row.td.text.strip()
                    product_info[key] = value
        
                book_dict['titles'].append(title)
                book_dict['genre'].append(genre_li)
                book_dict['ratings'].append(rating)
                book_dict['upc'].append(product_info.get('UPC', 'N/A'))  
                book_dict['product_type'].append(product_info.get('Product Type', 'N/A'))  
                book_dict['price_excl_tax_gbp'].append(product_info.get('Price (excl. tax)', 'N/A'))  
                book_dict['price_incl_tax_gbp'].append(product_info.get('Price (incl. tax)', 'N/A')) 
                book_dict['tax'].append(product_info.get('Tax', 'N/A')) 
                book_dict['in_stock'].append(product_info.get('Availability', 'N/A')) 
                book_dict['num_reviews'].append(product_info.get('Number of reviews', 'N/A')) 

            except Exception as e:
                print(f"Error processing book: {e}")
                continue

    books_raw_df=pd.DataFrame(book_dict)
    books_raw_df.to_csv('books_raw_data.csv')        
    
    return books_raw_df


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
    check_duplicates=books_raw_df.duplicated().sum()
    if check_duplicates !=0:
        books_raw_df=books_raw_df.drop_duplicates()

    check_null=books_raw_df.isnull().sum().sum()
    if check_null!=0:
        books_raw_df=books_raw_df.dropna()

    books_raw_df['titles']=books_raw_df['titles'].astype(str)
    books_raw_df['genre']=books_raw_df['genre'].astype(str)

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

    books_raw_df.to_csv('books_cleaned_data.csv')
    
    return books_raw_df


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
    unique_genres = books_clean_df['genre'].unique()
    unique_genres=[data.strip() for data in unique_genres]
    unique_genres=sorted(unique_genres)
    genre_to_id = {genre: idx for idx, genre in enumerate(unique_genres, start=1)}
    genre_df = pd.DataFrame({'id': list(genre_to_id.values()),'genre': list(genre_to_id.keys())})

    books_clean_df['genre']=books_clean_df['genre'].map(genre_to_id)
    books_clean_df=books_clean_df.rename(columns={'genre':'genre_id'})

    books_df=books_clean_df[['upc', 'titles', 'genre_id', 'ratings', 'product_type','price_excl_tax_gbp', 'price_incl_tax_gbp', 'tax', 'num_reviews']].copy()

    in_stock_df = books_clean_df[['upc', 'in_stock']].copy()

    books_df.to_csv('books.csv', index=False)
    genre_df.to_csv('genres.csv', index=False)
    in_stock_df.to_csv('in_stock.csv', index=False)

    return books_df, genre_df, in_stock_df


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
        conn = sqlite3.connect('books.db')
        books_df.to_sql('books', conn, if_exists='replace', index=False)
        genre_df.to_sql('genres', conn, if_exists='replace', index=False)
        in_stock_df.to_sql('in_stock', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


logger('Starting the ETL pipeline...')
logger('Extracting data from source...')
raw_data = extract()  
logger('Data extracted successfully.')    

logger('Cleaning and transforming the data...')
transforming_data = transform(raw_data)  
logger('Splitting data into normalized tables: books, genres, in_stock') 
books_df, genre_df, in_stock_df = normalize(transforming_data)
logger('Data cleaned and transformed successfully.') 

logger('Loading data into SQLite database...')
load(books_df,genre_df,in_stock_df)
logger('All data successfully loaded into the database.')
