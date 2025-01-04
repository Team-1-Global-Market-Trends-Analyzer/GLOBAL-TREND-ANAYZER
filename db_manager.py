import mysql.connector

# Function to insert market data into the SQL database
def insert_market_data(market_data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="market_data_db"
        )
        cursor = conn.cursor()

        # SQL query to insert data into the database
        insert_query = """
        INSERT INTO market_data (symbol, name, price, changes_percentage, change, day_low, day_high,
                                year_low, year_high, market_cap, price_avg_50, price_avg_200, volume, 
                                avg_volume, open, previous_close, eps, pe, earnings_announcement, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (
            market_data['symbol'],
            market_data['name'],
            market_data['price'],
            market_data['changesPercentage'],
            market_data['change'],
            market_data['dayLow'],
            market_data['dayHigh'],
            market_data['yearLow'],
            market_data['yearHigh'],
            market_data['marketCap'],
            market_data['priceAvg50'],
            market_data['priceAvg200'],
            market_data['volume'],
            market_data['avgVolume'],
            market_data['open'],
            market_data['previousClose'],
            market_data['eps'],
            market_data['pe'],
            market_data['earningsAnnouncement'],
            market_data['timestamp']
        )

        cursor.execute(insert_query, data)
        conn.commit()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Function to retrieve market data from the SQL database
def get_market_data(symbol):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="password",  # Replace with your MySQL password
            database="market_data_db"
        )
        cursor = conn.cursor()

        query = "SELECT * FROM market_data WHERE symbol = %s"
        cursor.execute(query, (symbol,))

        result = cursor.fetchall()

        if result:
            return result
        else:
            return "No data found."

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error fetching data."
