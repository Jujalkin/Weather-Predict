from app_1 import weather_score

use_cases = [
    {
        'temp': 1000000, #очень большая температура
        'humid': 70,
        'wind_speed': 10,
        'rain_prob': 45,
        'correct_answer': 'Ну и жарень! Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'
    },
    {
        'temp': -1000000, #очень маленькая температура
        'humid': 70,
        'wind_speed': 10,
        'rain_prob': 45,
        'correct_answer': 'Брр...А там прохладно(... Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'
    },
    {
        'temp': 10,
        'humid': 790, #очень большая влажность
        'wind_speed': 10,
        'rain_prob': 45,
        'correct_answer': 'Банька-парилка! Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'
    },
    {
        'temp': 10,
        'humid': 70,
        'wind_speed': 10000, #очень большая скорость ветра
        'rain_prob': 45,
        'correct_answer': 'Тебя сдует! Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'
    },
    {
        'temp': 10,
        'humid': 70,
        'wind_speed': 10,
        'rain_prob': 45000, #очень большая вероятность дождя
        'correct_answer': 'Очень-очень вероятно, что будет дождик) Ты точно уверен, что не хочешь посидеть под пледиком ДОМА?)'
    }
]


for case in use_cases:
    temp = case['temp']
    humid = case['humid']
    wind_speed = case['wind_speed']
    rain_prob = case['rain_prob']
    result = weather_score(temp, humid, wind_speed, rain_prob)
    if result == case['correct_answer']:
        print('Тест прошёл успешно!')