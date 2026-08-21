import requests

class CoinbaseCommerceAPI :
    def __init__ (self ,api_key ):
        self .api_key =api_key
        self .base_url ='https://api.commerce.coinbase.com/'

    def create_checkout (self ,name ,amount ,currency ,redirect_url ):
        headers ={
        'Content-Type':'application/json',
        'X-CC-Api-Key':self .api_key
        }
        data ={
        'name':name ,
        'local_price':{
        'amount':amount ,
        'currency':currency
        },
        'pricing_type':'fixed_price',
        'redirect_url':redirect_url
        }
        response =requests .post (self .base_url +'checkouts',headers =headers ,json =data )
        return response .json ()

    def get_checkout (self ,checkout_id ):

        headers ={
        'Content-Type':'application/json',
        'X-CC-Api-Key':self .api_key
        }
        response =requests .get (self .base_url +f'checkouts/{checkout_id}',headers =headers )
        return response .json ()

api_key ='your_coinbase_api_key'
commerce_api =CoinbaseCommerceAPI (api_key )
checkout =commerce_api .create_checkout ('Crypto Lending Service','100.00','USD','https://yourwebsite.com/checkout-success')
print (checkout )