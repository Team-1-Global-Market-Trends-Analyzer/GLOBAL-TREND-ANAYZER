import requests

def fetch_market_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # Adjust parsing based on API structure
    else:
        return None
    
    
# Function to fetch real-time market data from API
def fetch_real_time_market_data(api_url, params):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()  # Returns the raw JSON response from the API
    else:
        return {"error": "Failed to fetch data."}
