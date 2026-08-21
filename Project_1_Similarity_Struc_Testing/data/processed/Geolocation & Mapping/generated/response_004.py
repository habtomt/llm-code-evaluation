import cv2
import numpy as np
import requests
import json
from pygeocoder import Geocoder
import time

GOOGLE_MAPS_API_KEY ='YOUR_GOOGLE_MAPS_API_KEY'
MAPBOX_API_KEY ='YOUR_MAPBOX_API_KEY'

def get_current_location ():
    try :

        current_location =Geocoder (api_key =GOOGLE_MAPS_API_KEY )
        lat ,lng =current_location .latitude ,current_location .longitude
        return lat ,lng
    except Exception as e :
        print (f"Error getting current location: {e}")
        return None ,None

def get_navigation_directions (origin ,destination ):
    try :

        url =f'https://api.mapbox.com/directions/v5/mapbox/driving/{origin[1]},{origin[0]};{destination[1]},{destination[0]}?access_token={MAPBOX_API_KEY}'
        response =requests .get (url )
        data =json .loads (response .text )
        return data ['routes'][0 ]['geometry']['coordinates']
    except Exception as e :
        print (f"Error getting navigation directions: {e}")
        return None

def overlay_navigation_directions (camera_index ,navigation_directions ):
    try :

        cap =cv2 .VideoCapture (camera_index )

        if not cap .isOpened ():
            print ("Cannot open camera")
            return

        while True :

            ret ,frame =cap .read ()

            if not ret :
                print ("Cannot read frame")
                break

            for i in range (len (navigation_directions )-1 ):

                direction_vector =np .array ([navigation_directions [i +1 ][0 ]-navigation_directions [i ][0 ],navigation_directions [i +1 ][1 ]-navigation_directions [i ][1 ]])
                direction_vector =direction_vector /np .linalg .norm (direction_vector )

                cv2 .arrowedLine (frame ,(int (navigation_directions [i ][0 ]*100 ),int (navigation_directions [i ][1 ]*100 )),(int ((navigation_directions [i ][0 ]+direction_vector [0 ])*100 ),int ((navigation_directions [i ][1 ]+direction_vector [1 ])*100 )),(0 ,255 ,0 ),2 )

            cv2 .imshow ('Navigation',frame )

            if cv2 .waitKey (1 )&0xFF ==ord ('q'):
                break

        cap .release ()
        cv2 .destroyAllWindows ()
    except Exception as e :
        print (f"Error overlaying navigation directions: {e}")

def main ():

    current_lat ,current_lng =get_current_location ()

    destination_lat ,destination_lng =37.7749 ,-122.4194

    navigation_directions =get_navigation_directions ((current_lat ,current_lng ),(destination_lat ,destination_lng ))

    overlay_navigation_directions (0 ,navigation_directions )

if __name__ =="__main__":
    main ()