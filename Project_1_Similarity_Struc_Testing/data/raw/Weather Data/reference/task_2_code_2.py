`python

import requests

api_key = 'YOUR_API_KEY'

city = 'New York'

url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'



response = requests.get(url)

weather_data = response.json()



if weather_data['weather'][0]['main'] in ['Thunderstorm', 'Drizzle', 'Rain', 'Snow', 'Extreme']:

    # Implement notification functionality to alert users about severe weather conditions

    pass

    # Implement code for normal weather conditions

    pass