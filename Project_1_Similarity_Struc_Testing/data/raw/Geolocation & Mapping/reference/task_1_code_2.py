

from datetime import datetime

import googlemaps



# Initialize Google Maps API client

gmaps = googlemaps.Client(key='YOUR_API_KEY')



delivery_locations = [

    "1600 Amphitheatre Parkway, Mountain View, CA",

    "731 Lexington Avenue, New York, NY",

    "350 5th Ave, New York, NY"

]



# Get optimal route for the fleet of vehicles

directions = gmaps.directions(

    delivery_locations,

    optimize_waypoints=True,

    mode="driving",

    departure_time=now

)



# Display the optimized route

for leg in directions[0]['legs']:

    print(f"From {leg['start_address']} to {leg['end_address']}: {leg['duration']['text']} ({leg['distance']['text']})")