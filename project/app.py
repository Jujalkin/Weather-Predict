from flask import Flask, render_template, request
import requests
import os
from config import API_KEY



app = Flask(__name__)



def get_location_key(location):
    location_url = 'http://dataservice.accuweather.com/locations/v1/cities/autocomplete'
    params = {
        'apikey': API_KEY,
        'q': location,
        'language': 'ru-ru'
    }

    try:
        location_response = requests.get(location_url, params=params)
        location_response.raise_for_status()
        location_data = location_response.json()
        if location_data:
            return location_data[0]['Key']
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе локации: {e}')
        return None



def get_weather(location_key):
    weather_url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}'
    params = {
        'apikey': API_KEY,
        'language': 'ru-ru',
        'details': 'true',
        'metric': 'true'
    }

    try:
        weather_response = requests.get(weather_url, params=params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        if weather_data:
            return weather_data[0]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе погоды: {e}')
        return None