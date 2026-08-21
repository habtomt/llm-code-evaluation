import requests

API_KEY ='your_api_key'

API_SECRET ='your_api_secret'

API_ENDPOINT ='https://api.commerce.coinbase.com/'

def create_payment_order (price ,nft_id ,buyer_email ):

    headers ={

    'X-CC-Api-Key':API_KEY ,

    'X-CC-Version':'2018-03-22',

    'Content-Type':'application/json'

    }

    data ={

    'name':'NFT',

    'local_price':{

    'amount':price ,

    'currency':'USD'

    },

    'pricing_type':'fixed_price',

    'metadata':{

    'nft_id':nft_id ,

    'buyer_email':buyer_email

    }

    }

    response =requests .post (API_ENDPOINT +'charges',json =data ,headers =headers )

    return response .json ()