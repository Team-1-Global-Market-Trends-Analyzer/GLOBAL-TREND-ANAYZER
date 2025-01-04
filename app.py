import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from backend.database import init_db, insert_market_data, get_market_data
from backend.auth import validate_username, validate_password, authenticate_user
from backend.api_fetcher import fetch_real_time_market_data
import requests

# Initialize Database
init_db()

# Apply Purple Theme
st.markdown("<style>" + open('templates/purple_theme.css').read() + "</style>", unsafe_allow_html=True)

# App Title
st.title("🌎 Global Market Trends Analyzer")
st.sidebar.title("Navigation")
navigation = st.sidebar.radio(
    "Go to", 
    ["Login", "Register", "Dashboard", "Trend Analyzer", "Search & Comparative Analysis", "Admin"]
)

# Registration
if navigation == "Register":
    st.header("Register")
    username = st.text_input("Username (Min 4 characters)")
    password = st.text_input("Password (Min 6 characters)", type="password")
    if st.button("Register"):
        if validate_username(username) and validate_password(password):
            try:
                add_user(username, password)  # Ensure this function is defined in backend.auth
                st.success("User registered successfully!")
            except Exception:
                st.error("Username already exists!")
        else:
            st.error("Invalid username or password")

# Login
elif navigation == "Login":
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success(f"Welcome {username}!")
            st.session_state['user'] = username
        else:
            st.error("Invalid credentials")

# Dashboard
elif navigation == "Dashboard":
    if 'user' in st.session_state:
        st.header(f"Hello {st.session_state['user']}!")

        # Upload dataset
        uploaded_file = st.file_uploader("Upload your market data CSV", type=["csv"])
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            st.dataframe(data)

            # Filter data based on Region
            region = st.selectbox("Select Region", data['Region'].unique())
            filtered_data = data[data['Region'] == region]
            st.subheader(f"Showing Data for Region: {region}")
            st.dataframe(filtered_data)

            # Visualizations
            st.subheader("Market Trends")
            option = st.selectbox("Choose Visualization", ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap", "Scatter Plot"])

            if option == "Line Chart":
                fig = px.line(filtered_data, x='Date', y='Units Sold', title=f"Units Sold in {region}")
                st.plotly_chart(fig)

            elif option == "Bar Chart":
                fig = px.bar(filtered_data, x='Date', y='Units Sold', title=f"Units Sold in {region}")
                st.plotly_chart(fig)

            elif option == "Pie Chart":
                fig = px.pie(filtered_data, names='Category', values='Units Sold', title=f"Units Sold by Category in {region}")
                st.plotly_chart(fig)

            elif option == "Scatter Plot":
                fig = px.scatter(filtered_data, x='Units Sold', y='Price', color='Category', 
                                 title=f"Units Sold vs Price in {region}")
                st.plotly_chart(fig)
    else:
        st.error("Please log in to view the dashboard")

# Trend Analyzer
elif navigation == "Trend Analyzer":
    if 'user' in st.session_state:
        st.header(f"Market Trend Analyzer for {st.session_state['user']}")

        uploaded_file = st.file_uploader("Upload your market trend data CSV", type=["csv"])
        if uploaded_file:
            data = pd.read_csv(uploaded_file)
            st.dataframe(data)

            st.subheader("Filter Data by Date Range")
            start_date = st.date_input("Start Date", value=pd.to_datetime(data['Date']).min())
            end_date = st.date_input("End Date", value=pd.to_datetime(data['Date']).max())
            filtered_data = data[(pd.to_datetime(data['Date']) >= pd.to_datetime(start_date)) &
                                  (pd.to_datetime(data['Date']) <= pd.to_datetime(end_date))]
            st.dataframe(filtered_data)

            st.subheader("Filter Data by Region")
            regions = data['Region'].unique()
            selected_region = st.selectbox("Select Region", regions)
            region_data = filtered_data[filtered_data['Region'] == selected_region]
            st.dataframe(region_data)

            st.subheader("Market Trend Report")
            numeric_data = region_data.select_dtypes(include=['number'])
            if not numeric_data.empty:
                corr_matrix = numeric_data.corr()
                st.write("Correlation Matrix:")
                st.dataframe(corr_matrix)

                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
                st.pyplot(fig)
            else:
                st.error("No numeric data available for analysis.")
    else:
        st.error("Please log in to analyze trends")

# Admin
elif navigation == "Admin":
    st.header("Admin Dashboard")
    st.write("Perform CRUD operations here")

# Search & Comparative Analysis
import sqlite3
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Drop existing table
def drop_table():
    """Drop the market_data table if it exists."""
    connection = sqlite3.connect("market_data.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS market_data")
    connection.commit()
    connection.close()

# Create table
def create_table():
    """Create the database table if it doesn't already exist."""
    connection = sqlite3.connect("market_data.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            name TEXT,
            price REAL,
            exchange TEXT,
            exchangeShortName TEXT,
            type TEXT
        )
    """)
    connection.commit()
    connection.close()

# Insert market data
def insert_market_data(market_data):
    """Insert market data into the database."""
    connection = sqlite3.connect("market_data.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO market_data (symbol, name, price, exchange, exchangeShortName, type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (market_data['symbol'], market_data['name'], market_data['price'], 
          market_data['exchange'], market_data['exchangeShortName'], market_data['type']))
    connection.commit()
    connection.close()

# Fetch market data
def get_market_data(symbol):
    """Fetch market data from the database by symbol."""
    connection = sqlite3.connect("market_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM market_data WHERE symbol=?", (symbol,))
    row = cursor.fetchone()
    connection.close()
    if row:
        return {
            "id": row[0],
            "symbol": row[1],
            "name": row[2],
            "price": row[3],
            "exchange": row[4],
            "exchangeShortName": row[5],
            "type": row[6],
        }
    return None

# API function to fetch market data
def fetch_market_data(symbol):
    """Fetch market data from the Financial Modeling Prep API."""
    api_url = f"https://financialmodelingprep.com/api/v3/quote/{symbol}"
    params = {"apikey": "Vr7GK9iZYYV7vzRDzLaiQAndAtOmP61X"}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data:  # Ensure the API returned data
            return {
                "symbol": data[0].get("symbol"),
                "name": data[0].get("name"),
                "price": data[0].get("price"),
                "exchange": data[0].get("exchange"),
                "exchangeShortName": data[0].get("exchangeShortName"),
                "type": data[0].get("type"),
            }
    return None

# Display market data
def display_market_data(symbol):
    """Display market data from the database or API."""
    # First, try to fetch market data from the database
    data = get_market_data(symbol)

    if data:
        st.write(f"**Market Data for {data['name']} ({data['symbol']})**")
        st.write(f"**Price:** ${data['price']}")
        st.write(f"**Exchange:** {data['exchange']} ({data['exchangeShortName']})")
        st.write(f"**Type:** {data['type']}")
    else:
        # If not found in the database, fetch data from the API
        st.write(f"Fetching data for {symbol}...")
        market_data = fetch_market_data(symbol)

        if market_data:
            # Insert the new data into the database
            insert_market_data(market_data)

            # Display the fetched market data
            st.write(f"**Market Data for {market_data['name']} ({market_data['symbol']})**")
            st.write(f"**Price:** ${market_data['price']}")
            st.write(f"**Exchange:** {market_data['exchange']} ({market_data['exchangeShortName']})")
            st.write(f"**Type:** {market_data['type']}")
        else:
            st.error(f"No data found for {symbol}.")

# Display market trend using a line chart
def display_trend(symbol):
    """Fetch historical data and plot a trend line."""
    st.write(f"Fetching historical trend for {symbol}...")
    # Simulating trend data (use actual API for real data)
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    prices = [100 + i * 0.5 + (i % 5) * 2 for i in range(len(dates))]  # Simulated price trend

    # Plotting the trend
    trend_df = pd.DataFrame({"Date": dates, "Price": prices})
    st.line_chart(trend_df.set_index("Date"))

# Additional visualizations
def display_pie_chart():
    """Display a pie chart of market share of companies."""
    companies = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
    market_share = [45, 30, 15, 10]  # Simulated market share data

    fig, ax = plt.subplots()
    ax.pie(market_share, labels=companies, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    st.pyplot(fig)

def display_bar_chart():
    """Display a bar chart of stock prices for companies."""
    companies = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
    prices = [145, 2750, 3442, 298]  # Simulated stock prices

    fig, ax = plt.subplots()
    ax.bar(companies, prices, color=['blue', 'green', 'red', 'purple'])
    ax.set_title('Stock Prices of Companies')
    ax.set_xlabel('Companies')
    ax.set_ylabel('Price (USD)')
    st.pyplot(fig)

def display_scatter_plot():
    """Display a scatter plot for stock price vs volume."""
    companies = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
    stock_prices = [145, 2750, 3442, 298]  # Simulated stock prices
    volumes = [100000, 150000, 200000, 250000]  # Simulated trading volumes

    fig, ax = plt.subplots()
    ax.scatter(stock_prices, volumes, color='blue')
    ax.set_title('Stock Price vs Trading Volume')
    ax.set_xlabel('Stock Price (USD)')
    ax.set_ylabel('Trading Volume')
    st.pyplot(fig)

def display_histogram():
    """Display a histogram for stock price distribution."""
    stock_prices = [145, 2750, 3442, 298, 250, 3200, 115, 1400]  # Simulated stock prices

    fig, ax = plt.subplots()
    ax.hist(stock_prices, bins=5, color='green', edgecolor='black')
    ax.set_title('Stock Price Distribution')
    ax.set_xlabel('Stock Price (USD)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# Streamlit app
st.title("Global Market Trends Analyzer")
st.sidebar.header("Navigation")
navigation = st.sidebar.radio("Go to", ["Search & Comparative Analysis", "Dashboard", "Admin"])

# Drop the existing table and recreate it
drop_table()
create_table()

# Dashboard: Show an overview of market data and trend graphs
if navigation == "Dashboard":
    st.header("Dashboard")
    st.subheader("Top Companies Overview")

    # Show a list of market data for some companies (this can be dynamic or from the DB)
    symbols = ["AAPL", "GOOGL", "AMZN", "MSFT"]
    for symbol in symbols:
        st.write(f"**{symbol}**:")
        display_market_data(symbol)

    st.subheader("Market Visualizations")
    display_pie_chart()
    display_bar_chart()
    display_scatter_plot()
    display_histogram()

    st.subheader("Market Trends")
    company_symbol = st.selectbox("Select Company Symbol for Trend Analysis", symbols)
    if company_symbol:
        display_trend(company_symbol)

# Search & Comparative Analysis
if navigation == "Search & Comparative Analysis":
    st.header("Search & Comparative Analysis")
    company_symbol = st.text_input("Enter Company Symbol", "AAPL")  # Default to Apple

    if company_symbol:
        display_market_data(company_symbol)
