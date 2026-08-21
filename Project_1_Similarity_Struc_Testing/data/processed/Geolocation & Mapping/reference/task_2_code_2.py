import googlemaps

gmaps =googlemaps .Client (key ='YOUR_API_KEY')

geocode_result =gmaps .geocode ('1600 Amphitheatre Parkway, Mountain View, CA')

reverse_geocode_result =gmaps .reverse_geocode ((40.714224 ,-73.961452 ))

now =datetime .now ()

directions_result =gmaps .directions ("Sydney Town Hall",

"Parramatta, NSW",

mode ="transit",

departure_time =now )