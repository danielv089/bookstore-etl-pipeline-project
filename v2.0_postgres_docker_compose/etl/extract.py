import os
import requests
import time

import pandas as pd

from etl.logger import get_logger
from bs4 import BeautifulSoup

logger = get_logger(__name__)

def extract():
    """
    Extracts book data from the 'Books to Scrape' website.

    Scrapes **all catalog pages** and retrieves metadata for each book,
    including title, genre, rating, price, stock info, UPC, and number of reviews.
    The data is returned as a pandas DataFrame and also saved to 'extract_raw_data/books_raw_data.csv'.

    Returns:
        pd.DataFrame: A DataFrame containing raw book data.
    """
    book_dict={
        'titles':[], 'genre':[], 'ratings':[], 'upc':[], 'product_type':[],
        'price_excl_tax_gbp':[], 'price_incl_tax_gbp':[], 'tax':[], 'in_stock':[],
        'num_reviews':[]}

    page_num=1

    while True:
        try:
            url=f'https://books.toscrape.com/catalogue/page-{page_num}.html'
            response=requests.get(url)
            
            if response.status_code!=200:
                break 
                
            soup=BeautifulSoup(response.text, 'html.parser')
            books=soup.find_all('h3')
            logger.info(f'Scraping page {page_num}')

        except Exception as e:
            logger.error(f"Failed to load page {page_num}: {e}")
            continue    

        for book in books:
            try:
                a_tag=book.find('a')
                relative_link=a_tag['href']
                full_link='https://books.toscrape.com/catalogue/' + relative_link

                soup_2=BeautifulSoup(requests.get(full_link).text, 'html.parser')
                title=soup_2.find('li', class_='active').text.strip()
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
                logger.error(f"Error processing book: {e}")
                continue
                
        page_num+=1
        time.sleep(0.5)
            
    try:
        os.makedirs('data/1_extract_raw_data', exist_ok=True)
        books_raw_df=pd.DataFrame(book_dict)
        books_raw_df.to_csv('data/1_extract_raw_data/books_raw_data.csv', index=False)  
    except Exception as e:
        logger.error(f"Error saving extracted data: {e}")      
    
    return books_raw_df