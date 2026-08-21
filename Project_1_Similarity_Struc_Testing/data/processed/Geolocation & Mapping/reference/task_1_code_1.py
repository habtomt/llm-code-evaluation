import googlemaps

from datetime import datetime

gmaps =googlemaps .Client (key ='YOUR_API_KEY')

start_point ="Melbourne, Australia"

destinations =["Sydney, Australia","Brisbane, Australia","Adelaide, Australia"]

directions =gmaps .directions (start_point ,destinations ,mode ="driving",departure_time =now )

for step in directions [0 ]['legs']:

    print (step ['start_address']+" to "+step ['end_address']+": "+step ['duration']['text'])