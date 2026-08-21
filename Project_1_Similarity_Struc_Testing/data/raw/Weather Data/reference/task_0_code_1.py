`python

import requests



api_key = "YOUR_API_KEY"

city = "YOUR_CITY"

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"



response = requests.get(url)

data = response.json()



if data["cod"] == 200:

    temperature = data["main"]["temp"]

    humidity = data["main"]["humidity"]

    print(f"Temperature: {temperature}°C")

    print(f"Wind Speed: {wind_speed} m/s")

else:

    print("Error fetching data from OpenWeatherMap API")