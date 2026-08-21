import googlemaps

import cv2

import numpy as np

gmaps =googlemaps .Client (key ='your_api_key')

destination_geocode =gmaps .geocode ('Destination Address')

directions_result =gmaps .directions ('Origin Address','Destination Address')

cap =cv2 .VideoCapture (0 )

while True :

    ret ,frame =cap .read ()

    cv2 .imshow ('AR Navigation',frame )

    if cv2 .waitKey (1 )&0xFF ==ord ('q'):

        break

cv2 .destroyAllWindows ()