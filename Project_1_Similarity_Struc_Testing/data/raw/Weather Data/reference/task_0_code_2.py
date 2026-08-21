`python

import requests



API_KEY = "YOUR_API_KEY"

CITY = "New York"

UNITS = "metric"

URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&units={UNITS}&APPID={API_KEY}"



response = requests.get(URL)

data = response.json()

if response.status_code == 200:

    temperature = data['main']['temp']

    humidity = data['main']['humidity']

    wind_speed = data['wind']['speed']



    print(f"Temperature: {temperature}°C")

    print(f"Humidity: {humidity}%")

else:

    print("Error fetching data from OpenWeatherMap API")