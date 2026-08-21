import requests
import json

def fetch_product_details(product_id):
    url = f"https://example-store.myshopify.com/products/{product_id}.json"
    response = requests.get(url)
    product_data = response.json()
    return product_data

def update_price(product_id):
    product_data = fetch_product_details(product_id)
    new_price = product_data['variants'][0]['price']
    # Update price on the front-end

def display_product_description(description):
    # Display the product description on the front-end
    pass

def main():
    product_id = "12345"
    product_data = fetch_product_details(product_id)
    display_product_description(product_data['body_html'])
    update_price(product_id)
    # Implement AJAX call for dynamic content loading

if __name__ == "__main__":
    main()