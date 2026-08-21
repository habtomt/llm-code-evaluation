`python

import requests



# Replace 'your_api_key' with your actual OpenWeatherMap API key

API_KEY = 'your_api_key'



url = f'http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'



response = requests.get(url)

data = response.json()



if data['cod'] == 200:

    temperature = data['main']['temp']

    humidity = data['main']['humidity']

    weather_description = data['weather'][0]['description']

    if temperature > 20 and humidity > 60:

        print('Weather conditions are favorable for planting.')

    elif temperature > 25 and weather_description == 'clear sky':

        print('Weather conditions are optimal for harvesting.')

    else:

        print('Weather conditions are not suitable for any specific activity.')



else:

    print('Error while fetching weather data.')