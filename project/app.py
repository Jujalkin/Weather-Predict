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



def get_weather_info(weather_json):
    if weather_json:
        temp = weather_json['Temperature']['Value']
        humid = weather_json['RelativeHumidity']
        wind_speed = weather_json['Wind']['Speed']['Value']
        rain_prob = weather_json['RainProbability']
        return temp, humid, wind_speed, rain_prob
    else:
        return None


def weather_score(temp, humid, wind_speed, rain_prob):
    try:
        temp_text = ''
        if temp < 0: temp_text = 'Брр...А там прохладно(... '
        if temp > 35: temp_text = 'Ну и жарень! '

        humid_text = ''
        if humid > 85: humid_text = 'Банька-парилка! '

        wind_text = ''
        if wind_speed > 50: wind_text = 'Тебя сдует! '

        rain_text = ''
        if rain_prob > 70: rain_text = 'Очень-очень вероятно, что будет дождик) '

        if len(temp_text + humid_text + wind_text + rain_text) == 0:
            return 'Погода отличная! Можешь собираться в дорогу! '
        else:
            return temp_text + humid_text + wind_text + rain_text + 'Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'

    except Exception as e:
        print(f'Ошибка при вычислении погодного балла: {e}')
        return "Данные о погоде не найдены, проверьте корректность в названиях городов..."



@app.route('/', methods=['GET', 'POST'])
def weather_analysis():
    result = None
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']

        if not from_location or not to_location:
            result = "Пожалуйста, введите названия обоих городов."
        else:
            loc1_key = get_location_key(from_location)
            loc2_key = get_location_key(to_location)

            if loc1_key and loc2_key:
                weather1 = get_weather(loc1_key)
                weather2 = get_weather(loc2_key)

                forecast1 = get_weather_info(weather1)
                forecast2 = get_weather_info(weather2)

                if forecast1 and forecast2:
                    temp1, humid1, wind_speed1, rain_prob1 = forecast1
                    temp2, humid2, wind_speed2, rain_prob2 = forecast2

                    res1 = weather_score(temp1, humid1, wind_speed1, rain_prob1)
                    res2 = weather_score(temp2, humid2, wind_speed2, rain_prob2)

                    result = (f'Начальная точка: {res1}<br>'
                              f'Конечная точка: {res2}')
                else:
                    result = "Не удалось получить данные о погоде."
            else:
                result = "Не удалось найти указанные локации."

    return render_template('locations.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)