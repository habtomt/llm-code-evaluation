`python

import requests

def get_weather_data (api_key ,city ):

    url =f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response =requests .get (url )

    data =response .json ()

    return data

def get_event_suggestion (weather_data ):

    weather_description =weather_data ['weather'][0 ]['description']

    if "rain"in weather_description or "thunderstorm"in weather_description :

        return "Not suitable for outdoor events due to rain."

    elif temperature >25 :

        return "It's a hot day, consider planning events in the evening."

    elif 20 <=temperature <=25 :

        return "Weather looks good for outdoor events."

    else :

        return "Temperature is low, consider indoor events."

city ="London"

api_key ="YOUR_API_KEY"

weather_data =get_weather_data (api_key ,city )

if 'main'in weather_data :

    event_suggestion =get_event_suggestion (weather_data )

    print (event_suggestion )

else :

    print ("Failed to retrieve weather data.")