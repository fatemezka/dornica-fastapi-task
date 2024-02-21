from geopy.geocoders import Nominatim
import requests
import csv
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
load_dotenv()

WEATHERAPI_API_URL = os.getenv("WEATHERAPI_API_URL")
WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")
CURRENT_CITY_NAME = "Sari"


def get_weather_data(date):
    params = {
        'key': WEATHERAPI_API_KEY,
        'q': 'London',  # Replace 'CityName' with the name of the city you want weather data for
        'dt': date.strftime('%Y-%m-%d')
    }
    response = requests.get(WEATHERAPI_API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to fetch data for', date.strftime('%Y-%m-%d'))
        return None


def save_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ['Date', 'Max Temp (C)', 'Min Temp (C)', 'Condition'])  # Header row
        for day_data in data['forecast']['forecastday']:
            date = day_data['date']
            max_temp = day_data['day']['maxtemp_c']
            min_temp = day_data['day']['mintemp_c']
            condition = day_data['day']['condition']['text']
            writer.writerow([date, max_temp, min_temp, condition])


def main():
    start_date = datetime.now()

    end_date = start_date + timedelta(days=90)

    all_weather_data = []

    current_date = start_date
    while current_date <= end_date:
        weather_data = get_weather_data(current_date)
        if weather_data:
            all_weather_data.append(weather_data)
        current_date += timedelta(days=1)

    save_to_csv(all_weather_data, 'time.csv')
