import googlemaps

import requests

def get_geolocation (address ,api_key ):

    url ="https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}".format (address ,api_key )

    response =requests .get (url )

    data =response .json ()

    lat =data ['results'][0 ]['geometry']['location']['lat']

    lng =data ['results'][0 ]['geometry']['location']['lng']

    return (lat ,lng )

def get_navigation_instructions (origin ,destination ,api_key ):

    gmaps =googlemaps .Client (key =api_key )

    directions_result =gmaps .directions (origin ,destination )

    return directions_result

def overlay_navigation_on_camera_feed (navigation_instructions ,live_camera_feed ):

    pass

def navigate_to_destination (origin ,destination ,api_key ):

    origin_coords =get_geolocation (origin ,api_key )

    destination_coords =get_geolocation (destination ,api_key )

    navigation_instructions =get_navigation_instructions (origin ,destination ,api_key )

    overlay_navigation_on_camera_feed (navigation_instructions ,live_camera_feed )

api_key ='YOUR_GOOGLE_MAPS_API_KEY'

origin ='Times Square, New York, NY'

destination ='Central Park, New York, NY'

navigate_to_destination (origin ,destination ,api_key )