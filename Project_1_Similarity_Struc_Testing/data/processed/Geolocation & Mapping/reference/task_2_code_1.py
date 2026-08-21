import googlemaps

from datetime import datetime

api_key ='YOUR_API_KEY'

gmaps =googlemaps .Client (key =api_key )

location_data =gmaps .geolocate ()

incident_location =(latitude ,longitude )

directions =gmaps .directions (location_data ,incident_location ,mode ="driving")

print (directions )