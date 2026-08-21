import requests

api_key ='your_api_key'
api_secret ='your_api_secret'

base_url ='https://api.commerce.coinbase.com/'

def create_charge (amount ,currency ,name ,description ):
    endpoint ='charges'
    headers ={
    'Content-Type':'application/json',
    'X-CC-Api-Key':api_key ,
    'X-CC-Version':'2018-03-22'
    }
    data ={
    'name':name ,
    'description':description ,
    'local_price':{
    'amount':amount ,
    'currency':currency
    },
    'pricing_type':'fixed_price'
    }
    response =requests .post (base_url +endpoint ,headers =headers ,json =data )
    return response .json ()

def get_charge (charge_id ):
    endpoint =f'charges/{charge_id}'
    headers ={
    'Content-Type':'application/json',
    'X-CC-Api-Key':api_key ,
    'X-CC-Version':'2018-03-22'
    }
    response =requests .get (base_url +endpoint ,headers =headers )
    return response .json ()

def update_charge (charge_id ,new_name ):
    endpoint =f'charges/{charge_id}'

    headers ={
    'Content-Type':'application/json',
    'X-CC-Api-Key':api_key ,
    'X-CC-Version':'2018-03-22'
    }
    data ={
    'name':new_name
    }

    response =requests .put (base_url +endpoint ,headers =headers ,json =data )
    return response .json ()