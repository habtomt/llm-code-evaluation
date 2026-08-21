

import requests



# Replace with your actual API key and version

api_key = 'your_api_key'

api_version = '2018-03-22'



payload = {

    "name": "John Doe",

    "dob": "1990-01-01",

    "national_id": "1234567890"

}



# Replace with your actual merchant_id and API version

merchant_id = 'your_merchant_id'

api_url = f'https://api.commerce.coinbase.com/verify/identity/{merchant_id}'

headers = {

    'Content-Type': 'application/json',

    'X-CC-Api-Key': api_key,

    'X-CC-Version': api_version

}



response = requests.post(api_url, headers=headers, json=payload)



if response.status_code == 200:

    print('Identity verification successful')

    verification_result = response.json()

    print(verification_result)

    print('Identity verification failed')

    print(response.text)