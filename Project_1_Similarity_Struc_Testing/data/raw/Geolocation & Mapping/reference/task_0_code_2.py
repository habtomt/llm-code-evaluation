

import requests



api_key = 'YOUR_API_KEY'

radius = 1000

business_type = 'restaurant'



url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={user_location}&radius={radius}&type={business_type}&key={api_key}'



response = requests.get(url)

data = response.json()



for business in data['results']:

    business_location = business['vicinity']

    advertisement = f"Visit {business_name} located at {business_location}"

    print(advertisement)