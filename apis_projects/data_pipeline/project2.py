import requests
import pandas as pd
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Recheck the script
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY1")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY1")

def fetch_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        "city": data["name"],
        "temperature": data["main"]["temp"]
    }

def fetch_news(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}"
    response = requests.get(url)
    return response.json()["articles"]

def transform_weather(data):
    return pd.DataFrame([{
        "city": data["city"],
        "temperature": data["temperature"],
        "timestamp": datetime.now()
    }])

def transform_news(articles):
    return pd.DataFrame([{
        "title": article["title"],
        "source": article["source"]["name"],
        "published_at": article["publishedAt"]
    } for article in articles])

def load_to_db(df, table_name):  # Remember to create a database first before doing this loading data process
    conn = sqlite3.connect("data.db")
    df.to_sql(table_name, conn,if_exists="append",index=False)
    conn.close()

# Run the pipeline
weather_data = fetch_weather("London")
weather_df = transform_weather(weather_data)
load_to_db(weather_df,"weather")

news_data = fetch_news("technology")
news_df = transform_news(news_data)
load_to_db(news_df,"news")