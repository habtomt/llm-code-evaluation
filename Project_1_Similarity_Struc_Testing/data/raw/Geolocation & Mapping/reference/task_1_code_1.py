

import googlemaps

from datetime import datetime



gmaps = googlemaps.Client(key='YOUR_API_KEY')

# Define starting point and destinations

start_point = "Melbourne, Australia"

destinations = ["Sydney, Australia", "Brisbane, Australia", "Adelaide, Australia"]



# Calculate optimal delivery route

directions = gmaps.directions(start_point, destinations, mode="driving", departure_time=now)



# Print the optimized delivery route

for step in directions[0]['legs']:

    print(step['start_address'] + " to " + step['end_address'] + ": " + step['duration']['text'])