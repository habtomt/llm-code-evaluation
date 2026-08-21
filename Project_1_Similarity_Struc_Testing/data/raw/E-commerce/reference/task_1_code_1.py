import requests
import json

class ShopifyAPI:
    def __init__(self, api_key, api_secret, store_url):
        self.api_key = api_key
        self.api_secret = api_secret
        self.store_url = store_url
        self.access_token = None

    def get_access_token(self):
        auth_url = f"https://{self.store_url}/admin/oauth/access_token"
        auth_data = {
            "client_id": self.api_key,
            "client_secret": self.api_secret,
            "code": "authorization_code"
        }
        response = requests.post(auth_url, data=auth_data)
        self.access_token = response.json()["access_token"]

    def get_cart(self, customer_id):
        cart_url = f"https://{self.store_url}/admin/api/2026-07/customers/{customer_id}/cart.json"
        headers = {
            "X-Shopify-Access-Token": self.access_token
        }
        response = requests.get(cart_url, headers=headers)
        return response.json()

    def add_to_cart(self, customer_id, product_id, quantity):
        cart_url = f"https://{self.store_url}/admin/api/2026-07/customers/{customer_id}/cart/add.js"
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "items": [
                {
                    "id": product_id,
                    "quantity": quantity
                }
            ]
        }
        response = requests.post(cart_url, headers=headers, data=json.dumps(payload))
        return response.json()

    def remove_from_cart(self, customer_id, line_item_id):
        cart_url = f"https://{self.store_url}/admin/api/2026-07/customers/{customer_id}/cart/remove.json"
        headers = {
            "X-Shopify-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "id": line_item_id
        }
        response = requests.post(cart_url, headers=headers, data=json.dumps(payload))
        return response.json()