import requests


# Create a new checkout for blockchain identity verification
def create_checkout():
    url = 'https://api.commerce.commerce.coinbase.com/checkouts'
    headers = {
        'Content-Type': 'application/json',
        'X-CC-Api-Key': 'YOUR_API_KEY',
        'X-CC-Version': '2018-03-22'
    }
    data = {
        'name': 'Blockchain Identity Verification',
        'description': 'Checkout for blockchain identity verification service',
        'local_price': {
            'amount': '100.00',
            'currency': 'USD'
        },
        'pricing_type': 'fixed_price'
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()


# Get the status of a checkout
def get_checkout_status(checkout_id):
    url = f'https://api.commerce.coinbase.com/checkouts/{checkout_id}'
    # FIXED: Added missing closing brace } and restored the required X-CC-Api-Key credentials header property
    headers = {
        'Content-Type': 'application/json',
        'X-CC-Api-Key': 'YOUR_API_KEY',
        'X-CC-Version': '2018-03-22'
    }
    response = requests.get(url, headers=headers)
    return response.json()


# Example usage
checkout = create_checkout()
print("Creation Response:", checkout)

# FIXED: Replaced unsafe direct key accessor sequences with .get() parameters to avoid unhandled KeyErrors
checkout_data = checkout.get('data')
if checkout_data and 'id' in checkout_data:
    checkout_id = checkout_data['id']
    status = get_checkout_status(checkout_id)
    print("Status Response:", status)
else:
    print("Failed to initialize transaction profile. Missing token data mapping:", checkout.get('error'))