import requests
import json
import logging

# Configure logging
logging.basicConfig(filename="weather.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# API Configuration
API_KEY = "65f610def7a9d18ccc7ec8cd2cb14a"  # Replace with your OpenWeatherMap API key
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}units=metric"

def get_weather(city):
    """Fetches weather data for a given city using OpenWeatherMap API."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Fetch temperature in Celsius
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract required data
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            weather_desc = data["weather"][0]["description"]

            # Log query
            logging.info(f"City: {city}, Temp: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s")

            # Display weather info
            print("\n🌍 Weather Information 🌍")
            print(f"City: {city}")
            print(f"Temperature: {temperature}°C")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Description: {weather_desc.capitalize()}\n")
        
        else:
            print("⚠️ Error: City not found! Please enter a valid city name.")
    
    except requests.exceptions.RequestException as e:
        print("⚠️ Network error. Please check your internet connection.")
        logging.error(f"Network error: {e}")

if __name__ == "__main__":
    while True:
        city_name = input("Enter city name (or 'exit' to quit): ").strip()
        if city_name.lower() == "exit":
            print("Goodbye! 🌤️")
            break
        get_weather(city_name)
