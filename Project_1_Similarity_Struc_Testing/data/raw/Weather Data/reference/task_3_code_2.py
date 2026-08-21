`python

import requests



def get_weather_forecast(city, api_key):

    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {

        "q": city,

        "appid": api_key,

        "units": "metric"

    }

    response = requests.get(base_url, params=params)

    data = response.json()

    if response.status_code == 200:

        temperature = data["main"]["temp"]

        condition = data["weather"][0]["description"]

        return temperature, condition

    else:



def suggest_optimal_event_time(city, api_key):

    temperature, condition = get_weather_forecast(city, api_key)

    if temperature is not None and condition is not None:

        if condition == "clear sky" and temperature > 15:

            return "Optimal time for outdoor event"

        else:

            return "Consider indoor event or choose a different time"

    else:

        return "Failed to fetch weather data"



city = "New York"

api_key = "your_api_key"