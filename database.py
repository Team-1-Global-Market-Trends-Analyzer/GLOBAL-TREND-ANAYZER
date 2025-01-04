# backend/database.py
import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY,
        symbol TEXT,
        name TEXT,
        price REAL,
        exchange TEXT,
        exchangeShortName TEXT,
        type TEXT
    )
    """)
    conn.commit()
    conn.close()

# Insert market data into the database
def insert_market_data(data):
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO market_data (symbol, name, price, exchange, exchangeShortName, type)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (data["symbol"], data["name"], data["price"], data["exchange"], data["exchangeShortName"], data["type"]))
    conn.commit()
    conn.close()

# Retrieve market data from the database
def get_market_data(symbol):
    conn = sqlite3.connect("market_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM market_data WHERE symbol=?", (symbol,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {
            "symbol": result[1],
            "name": result[2],
            "price": result[3],
            "exchange": result[4],
            "exchangeShortName": result[5],
            "type": result[6]
        }
    return None
