`python

import requests

api_key ="YOUR_API_KEY"

city_name ="CITY_NAME"

country_code ="COUNTRY_CODE"

url =f"http://api.openweathermap.org/data/2.5/weather?q={city_name},{country_code}&appid={api_key}"

response =requests .get (url )

data =response .json ()

if response .status_code ==200 :

    temperature =data ['main']['temp']

    humidity =data ['main']['humidity']

    wind_speed =data ['wind']['speed']

    weather_description =data ['weather'][0 ]['description']

    print (f"Temperature: {temperature}K")

    print (f"Humidity: {humidity}%")

    print (f"Weather: {weather_description}")

else :

    print ("Failed to fetch weather data")