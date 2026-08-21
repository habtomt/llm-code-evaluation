`python

import requests



def get_weather_alerts(api_key, city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)

    data = response.json()



    if data['weather'][0]['main'] in ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Tornado', 'Squall', 'Mist', 'Smoke', 'Haze', 'Dust', 'Fog', 'Sand', 'Ash', 'Squall']:

    else:



api_key = "YOUR_API_KEY"

city = "YOUR_CITY"

print(get_weather_alerts(api_key, city))