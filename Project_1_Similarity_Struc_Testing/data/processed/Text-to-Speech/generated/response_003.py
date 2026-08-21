import googlemaps
import pyttsx3
import time
import threading

gmaps =googlemaps .Client (key ='YOUR_GOOGLE_MAPS_API_KEY')

engine =pyttsx3 .init ()

def get_directions (origin ,destination ):
    try :
        directions_result =gmaps .directions (origin ,destination ,mode ="driving")
        if directions_result :
            steps =directions_result [0 ]['legs'][0 ]['steps']
            return steps
        else :
            return []
    except Exception as e :
        print (f"Error retrieving directions: {str(e)}")
        return []

def offer_spoken_directions (origin ,destination ):
    steps =get_directions (origin ,destination )

    if not steps :
        engine .say ("I could not retrieve the directions.")
        engine .runAndWait ()
        return

    for step in steps :

        instruction =step ['html_instructions']

        cleaned_instruction =instruction .replace ('<b>','').replace ('</b>','').replace ('<div style="font-size:0.9em">',' ').replace ('</div>','')

        engine .say (cleaned_instruction )
        engine .runAndWait ()
        time .sleep (2 )

    engine .say ("You have arrived at your destination.")
    engine .runAndWait ()

def update_location (origin ,destination ):
    while True :
        try :

            current_location =gmaps .geocode (origin )
            if current_location :
                engine .say (f"Current location: {current_location[0]['formatted_address']}")
                engine .runAndWait ()
            time .sleep (5 )
        except Exception as e :
            print (f"Error updating location: {str(e)}")
            time .sleep (5 )

origin ="Times Square, New York, NY"
destination ="Central Park, New York, NY"

location_thread =threading .Thread (target =update_location ,args =(origin ,destination ))
location_thread .daemon =True
location_thread .start ()

offer_spoken_directions (origin ,destination )

while True :
    pass