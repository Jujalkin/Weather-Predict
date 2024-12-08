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