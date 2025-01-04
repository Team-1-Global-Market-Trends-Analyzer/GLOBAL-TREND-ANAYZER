from backend.auth import validate_username, validate_password
import pytest
import sqlite3
from backend.database import add_user, get_user
from sqlalchemy import create_engine
from backend.api_fetcher import fetch_real_time_market_data

DATABASE_URL = "sqlite:///market_data.db"  # Change this to your database
engine = create_engine(DATABASE_URL)


def test_validate_username():
    assert validate_username("user") == True
    assert validate_username("abc") == False

def test_validate_password():
    assert validate_password("pass12") == True
    assert validate_password("123") == False

def test_add_user():
    add_user("testuser", "testpassword")
    conn = sqlite3.connect('market_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username='testuser'")
    user = c.fetchone()
    assert user is not None
    conn.close()




def test_fetch_real_time_market_data():
    api_url = "https://financialmodelingprep.com/api/v3/quote"
    params = {"symbol": "AAPL", "apikey": "your_api_key"}
    
    data = fetch_real_time_market_data(api_url, params)
    
    assert "error" not in data, f"Error fetching data: {data.get('error', 'Unknown error')}"
    assert "price" in data[0], "Price data not found in the response."
