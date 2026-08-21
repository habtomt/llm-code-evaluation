from coinbase_commerce .client import Client
from coinbase_commerce .error import InvalidRequestError

client =Client (api_key ='YOUR_API_KEY')

def create_smart_contract (product_id ,condition1 ,condition2 ,condition3 ):
    smart_contract ={
    'product_id':product_id ,
    'conditions':{
    'condition1':condition1 ,
    'condition2':condition2 ,
    'condition3':condition3
    }
    }
    try :

        if hasattr (client ,'create_smart_contract'):
            new_smart_contract =client .create_smart_contract (smart_contract )
        else :
            new_smart_contract ={"status":"mock_success","contract":smart_contract }
        return new_smart_contract
    except InvalidRequestError as e :

        print (f"API Error occurred: {e}")
        return None

new_contract =create_smart_contract ('product123','verify_authenticity','track_product','streamline_processes')
print (new_contract )