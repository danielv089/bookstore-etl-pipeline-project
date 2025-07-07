# Python ETL Project: Scraping, Transforming, and Loading Book Data

## 📌 Overview
This project is a complete **ETL (Extract, Transform, Load) pipeline** built in Python.  
It scrapes book data from the web, cleans and normalizes it, and loads it into a SQL database.  
The goal is to demonstrate a practical, end-to-end data engineering workflow using Python and containerization with Docker.

## ⚙️ ETL Pipeline Steps

### 1️⃣ Extract
- Scrapes all catalog pages from [Books to Scrape](https://books.toscrape.com/).
- Retrieves metadata: title, genre, rating, price, stock availability, UPC, and number of reviews.
- Saves raw data to 1_extract_raw_data


### 2️⃣ Transform
- Removes duplicates and null values
- Standardizes data types and formats
- Reclassifies Default and Add a comment genrew into Uncategorized
- Maps rating strings to numerical values
- Cleans currency symbols and parses stock quantities
- Saves cleaned data to 2_transform_data/books_cleaned_data.csv/books_raw_data.csv

### 3️⃣ Normalize
- Extracts a genre lookup table
- Replaces genre strings with foreign key IDs
- Splits in_stock data into its own table
- Saves normalized CSV files to 3_normalized_data/

### 4️⃣ Load
- Loads normalized tables into a SQL database

  ![ETL Pipeline Diagram](docs/etl_project.jpg)


## 🐳 Docker Support
This ETL pipeline is containerized for easier deployment.

**Build the Docker image:**

docker build -t  v1.5_sqlite

**Run the Docker container with volumes to map folders inside the container to folders on the host machine:**

docker run -it --rm -v "$PWD/data":/app/data -v "$PWD/logs":/app/logs v1.5_sqlite


## 🔄 Versions

- **v1.5 – Python, SQLite and Docker**

- **v1.4 – Python and SQLite**

  [Changelog](CHANGELOG.md)

## 🧰 Tech Stack
- **Python**
- **Pandas** 
- **Requests**
- **BeautifulSoup4**
- **SQLite3** 
- **Logging**
- **Docker**
- **Pytest**

## 🔗 References

- Books to Scrape
https://books.toscrape.com/

- Pandas Documentation
https://pandas.pydata.org/docs/

- BeautifulSoup Documentation
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

- Requests Library
https://docs.python-requests.org/

- SQLite3
https://docs.python.org/3/library/sqlite3.html

- Python Logging Module
https://docs.python.org/3/library/logging.html

- Docker Documentation
https://docs.docker.com/

- PostgreSQL Documentation
https://www.postgresql.org/docs/

✅ This project uses only publicly available data for educational purposes.
