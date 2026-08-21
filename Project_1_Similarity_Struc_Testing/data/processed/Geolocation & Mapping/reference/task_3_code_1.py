import googlemaps

gmaps =googlemaps .Client (key ='YOUR_API_KEY')

def track_activity (activity ):
    if activity =='running':

        pass
    elif activity =='cycling':

        pass
    else :
        print ("Invalid activity")

activity_type ='running'
track_activity (activity_type )