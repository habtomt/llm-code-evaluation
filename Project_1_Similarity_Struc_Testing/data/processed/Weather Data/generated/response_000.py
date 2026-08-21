import os
import requests
from flask import Flask ,render_template

app =Flask (__name__ )

API_KEY ='YOUR_API_KEY'
BASE_URL ='https://api.openweathermap.org/data/2.5/weather'

def get_weather_data (city_name ):
    try :
        params ={
        'q':city_name ,
        'appid':API_KEY ,
        'units':'metric'
        }
        response =requests .get (BASE_URL ,params =params )
        response .raise_for_status ()
        return response .json ()
    except requests .RequestException as e :
        print (f"Error fetching weather data: {e}")
        return None

@app .route ('/')
def home ():
    city_name ='New York'
    weather_data =get_weather_data (city_name )

    if weather_data and weather_data ['cod']==200 :
        main =weather_data ['main']
        wind =weather_data ['wind']
        weather ={
        'city':city_name ,
        'temperature':main ['temp'],
        'humidity':main ['humidity'],
        'wind_speed':wind ['speed'],
        'weather_description':weather_data ['weather'][0 ]['description'],
        }
    else :
        weather =None
    return render_template ('dashboard.html',weather =weather )

@app .route ('/city/<city_name>')
def get_city_weather (city_name ):
    weather_data =get_weather_data (city_name )

    if weather_data and weather_data ['cod']==200 :
        main =weather_data ['main']
        wind =weather_data ['wind']
        weather ={
        'city':city_name ,
        'temperature':main ['temp'],
        'humidity':main ['humidity'],
        'wind_speed':wind ['speed'],
        'weather_description':weather_data ['weather'][0 ]['description'],
        }
    else :
        weather =None
    return render_template ('dashboard.html',weather =weather )

if __name__ =='__main__':
    app .run (debug =True )