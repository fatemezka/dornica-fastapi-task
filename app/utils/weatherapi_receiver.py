import requests
import csv
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("WEATHERAPI_API_KEY")
WEATHERAPI_API_URL = os.getenv("WEATHERAPI_API_URL")
url = f"{WEATHERAPI_API_URL}/forecast.json?key={API_KEY}&q=sari&dt="


# Function to fetch weather data for a specific date
def fetch_weather_data(date):
    response = requests.get(url + date)
    data = response.json()
    return data


# Function to save weather data to time.csv
def save_to_csv(data):
    with open('time.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Max Temp (C)', 'Min Temp (C)',
                        'Avg Temp (C)', 'Max Wind (km/h)', 'Total Precipitation (mm)'])
        for date, info in data.items():
            if 'error' in info:
                print(f"Error for date {date}: {info['error']['message']}")
            else:
                writer.writerow([date, info['forecast']['forecastday'][0]['day']['maxtemp_c'], info['forecast']['forecastday'][0]['day']['mintemp_c'], info['forecast']
                                ['forecastday'][0]['day']['avgtemp_c'], info['forecast']['forecastday'][0]['day']['maxwind_kph'], info['forecast']['forecastday'][0]['day']['totalprecip_mm']])


# Function to generate date strings for the next 10 days
def generate_dates():
    current_date = datetime.now()
    end_date = current_date + timedelta(days=10)
    dates = []
    while current_date < end_date:
        dates.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return dates


def main():
    dates = generate_dates()
    weather_data = {}

    for date in dates:
        weather_data[date] = fetch_weather_data(date)

    save_to_csv(weather_data)
