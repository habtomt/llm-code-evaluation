import requests
import json
import geocoder
import folium

def get_user_location ():
    try :
        g =geocoder .ip ('me')
        return g .lat ,g .lng
    except Exception as e :
        print (f"Error getting user location: {e}")
        return None

def fetch_nearby_businesses (lat ,lng ,api_key ='YOUR_API_KEY'):
    try :
        url =f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=1000&type=restaurant&key={api_key}'
        response =requests .get (url )
        data =json .loads (response .text )
        return data ['results']
    except Exception as e :
        print (f"Error fetching businesses: {e}")
        return []

def deliver_advertisements (businesses ):

    for business in businesses :
        if should_show_ad (business ):
            show_ad_for_business (business )

def should_show_ad (business ):

    return True

def show_ad_for_business (business ):

    print (f"Showing ad for business: {business['name']}")

def create_map (businesses ,lat ,lng ):
    m =folium .Map (location =[lat ,lng ],zoom_start =15 )
    for business in businesses :
        folium .Marker ([business ['geometry']['location']['lat'],business ['geometry']['location']['lng']],popup =business ['name']).add_to (m )
    return m

def main ():
    lat ,lng =get_user_location ()
    if lat and lng :
        businesses =fetch_nearby_businesses (lat ,lng )
        deliver_advertisements (businesses )
        m =create_map (businesses ,lat ,lng )
        m .save ('map.html')

if __name__ =="__main__":
    main ()