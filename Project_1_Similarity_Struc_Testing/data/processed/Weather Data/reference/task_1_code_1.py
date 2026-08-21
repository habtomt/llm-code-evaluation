`python

import requests

url ="https://api.openweathermap.org/data/2.5/onecall/timemachine"

params ={

"lat":YOUR_LATITUDE ,

"lon":YOUR_LONGITUDE ,

"start":START_TIMESTAMP ,

"end":END_TIMESTAMP ,

"appid":"YOUR_API_KEY"

}

response =requests .get (url ,params =params )

    weather_data =response .json ()

else :

    print ("Failed to retrieve historical weather data")