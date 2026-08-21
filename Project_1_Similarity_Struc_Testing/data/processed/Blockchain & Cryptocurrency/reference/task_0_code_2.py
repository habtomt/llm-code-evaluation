import requests

API_KEY ='your_api_key'

API_VERSION ='2018-03-22'

HEADERS ={

'Content-Type':'application/json',

'X-CC-Api-Key':API_KEY ,

}

def create_checkout (price ,currency ,name ,description ):

    data ={

    'name':name ,

    'description':description ,

    'local_price':{

    'amount':price ,

    'currency':currency

    },

    'pricing_type':'fixed_price',

    'requested_info':['name','email']
    }

    response =requests .post (f'{API_URL}/checkouts',json =data ,headers =HEADERS )

    return response .json ()

def get_checkout (checkout_id ):

    response =requests .get (f'{API_URL}/checkouts/{checkout_id}',headers =HEADERS )

    return response .json ()

def create_charge (checkout_id ):

    data ={}

    response =requests .post (f'{API_URL}/checkouts/{checkout_id}/create-charge',json =data ,headers =HEADERS )

    return response .json ()

checkout =create_checkout (100 ,'USD','Product Name','Product Description')

checkout_id =checkout ['id']

charge =create_charge (checkout_id )

print (charge )