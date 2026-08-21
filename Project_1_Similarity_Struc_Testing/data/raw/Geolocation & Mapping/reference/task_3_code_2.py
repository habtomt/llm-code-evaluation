

from datetime import datetime



gmaps = googlemaps.Client(key='YOUR_API_KEY')



# Define the user's start and end location, and the mode of transportation

start_location = (40.7128, -74.0060)

end_location = (34.0522, -118.2437)

mode = "bicycling"



# Get the directions and route information

now = datetime.now()

directions = gmaps.directions(start_location, end_location, mode=mode, departure_time=now)



distance = directions[0]['legs'][0]['distance']['text']

duration = directions[0]['legs'][0]['duration']['text']



print(f"Distance: {distance}, Duration: {duration}")