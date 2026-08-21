# Import necessary libraries
import requests
import json

# Define the Shopify API base URL and endpoints
base_url = "https://your-store.myshopify.com"
cart_url = f'{base_url}/cart.js'

# Make a request to fetch the current cart state
def get_cart():
    response = requests.get(cart_url)
    return response.json()

# Send a request to add an item to the cart
def add_to_cart(item_id, quantity=1):
    payload = {
        'id': item_id,
        'quantity': quantity
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(cart_url, data=json.dumps(payload), headers=headers)
    return response.json()

# Send a request to remove an item from the cart
def remove_from_cart(item_id):
    payload = {
        'id': item_id,
        'quantity': 0
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(cart_url, data=json.dumps(payload), headers=headers)
    return response.json()

# Calculate the cart total dynamically (Shopify prices are typically in cents)
def calculate_total(cart):
    total = 0
    for item in cart.get('items', []):
        total += float(item.get('price', 0)) * item.get('quantity', 0)
    return total