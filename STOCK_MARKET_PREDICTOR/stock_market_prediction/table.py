import streamlit as st
import requests
import pandas as pd
import schedule
import time
import threading
import pytz
from datetime import datetime

# Define the API URL
api_url = "http://127.0.0.1:8000/api/scrape/"

# Nepali timezone
nepal_tz = pytz.timezone('Asia/Kathmandu')

# Fetch data from the API
def fetch_data():
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse JSON data
        df = pd.DataFrame(data)
        df.to_csv("latest_stock_data.csv", index=False)  # Save the latest data to a CSV file
        st.success("Data successfully fetched and saved!")
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Load data from the CSV file
def load_data():
    try:
        df = pd.read_csv("latest_stock_data.csv")
        return df
    except FileNotFoundError:
        st.error("No data available. Please fetch the data first.")
        return None

# Display data in Streamlit
def display_data(df):
    if df is not None:
        # Display the DataFrame in a table
        st.write("## Today's Stock Market Data")
        st.dataframe(df)

    else:
        st.error("No data to display.")

# Scheduler to update data daily at 3 PM NPT
def schedule_api_call():
    schedule.every().day.at("15:00").do(fetch_data)  # Nepali stock market closes at 3 PM

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

# Run scheduler in a separate thread
def start_scheduler():
    scheduler_thread = threading.Thread(target=schedule_api_call)
    scheduler_thread.daemon = True
    scheduler_thread.start()

# Streamlit App
def main():
    st.title("Stock Market Data")

    # Start the scheduler when the app starts
    start_scheduler()

    # Load and display data
    df = load_data()
    display_data(df)

    # Option to manually fetch data
    if st.button("Fetch Latest Data Now"):
        df = fetch_data()
        display_data(df)

if __name__ == "__main__":
    main()
