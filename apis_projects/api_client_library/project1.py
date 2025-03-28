import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_current_weather(self,city):
        """Fetch current weather for a given city"""
        url = f"{self.base_url}/weather?q={city}&appid={self.api_key}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

# Usage
client = WeatherClient(API_KEY)
print(client.get_current_weather("London")) # Fetching "London" weather information