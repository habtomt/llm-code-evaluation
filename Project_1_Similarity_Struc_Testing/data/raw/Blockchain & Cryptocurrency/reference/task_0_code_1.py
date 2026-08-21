
import requests



api_key = 'your_api_key'

base_url = 'https://api.commerce.coinbase.com/'



def create_charge(amount, currency, name, description):

    url = base_url + 'charges'

    headers = {'X-CC-Api-Key': api_key, 'Content-Type': 'application/json'}

    payload = {

        'description': description,

        'local_price': {

            'amount': amount,

            'currency': currency

        },

        'pricing_type': 'fixed_price',

        'metadata': {

            'customer_id': 'id_1005',

        }

    }

    response = requests.post(url, headers=headers, json=payload)

    return response.json()



def check_charge(charge_id):

    url = base_url + f'charges/{charge_id}'

    headers = {'X-CC-Api-Key': api_key}

    response = requests.get(url, headers=headers)

    return response.json()



# Example usage

charge = create_charge('10.00', 'USD', 'Sample Charge', 'Test charge for cryptocurrency payment')

print(charge)



# Use the returned charge ID to check the status of the charge

# charge_id = charge['data']['id']

# checked_charge = check_charge(charge_id)

# print(checked_charge)