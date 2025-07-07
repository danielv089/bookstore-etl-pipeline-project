import os
import sqlite3
import pandas as pd
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_extract():
    extract_csv_path = os.path.join(PROJECT_ROOT, "data/1_extract_raw_data/books_raw_data.csv")
    assert os.path.isfile(extract_csv_path), "Extract CSV file does not exist"

    df = pd.read_csv(extract_csv_path)
    assert not df.empty, "Extract CSV file is empty"


def test_transform():
    transform_csv_path = os.path.join(PROJECT_ROOT, "data/2_transform_data/books_cleaned_data.csv")
    assert os.path.isfile(transform_csv_path), "Transform CSV file does not exist"

    df = pd.read_csv(transform_csv_path)
    assert not df.empty, "Transform CSV file is empty"


def test_normalize():
    books_csv_path = os.path.join(PROJECT_ROOT, "data/3_normalized_data/books.csv")
    genres_csv_path = os.path.join(PROJECT_ROOT, "data/3_normalized_data/genres.csv")
    in_stock_csv_path = os.path.join(PROJECT_ROOT, "data/3_normalized_data/in_stock.csv")

    assert os.path.isfile(books_csv_path), "books.csv does not exist"
    assert os.path.isfile(genres_csv_path), "genres.csv does not exist"
    assert os.path.isfile(in_stock_csv_path), "in_stock.csv does not exist"

    books_df = pd.read_csv(books_csv_path)
    genres_df = pd.read_csv(genres_csv_path)
    in_stock_df = pd.read_csv(in_stock_csv_path)

    assert not books_df.empty, "books.csv is empty"
    assert not genres_df.empty, "genres.csv is empty"
    assert not in_stock_df.empty, "in_stock.csv is empty"


def test_load():
    db_path = os.path.join(PROJECT_ROOT, "data/4_database/books.db")
    assert os.path.isfile(db_path), "Database file does not exist"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM books;")
    count = cursor.fetchone()[0]
    assert count > 0, "Table 'books' is empty"

    conn.close()
