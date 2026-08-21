`python

import requests

import matplotlib.pyplot as plt



api_key = 'YOUR_API_KEY'

city = 'YOUR_CITY'

start_date = 'START_DATE'  # Format: 'YYYY-MM-DD'



url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}'



response = requests.get(url)

data = response.json()



temperatures = [temp['main']['temp'] for temp in data['list']]



plt.figure(figsize=(10, 6))

plt.plot(dates, temperatures, marker='o')

plt.title('Temperature Trend')

plt.xlabel('Date')

plt.ylabel('Temperature (K)')

plt.xticks(rotation=45)

plt.grid(True)

plt.show()