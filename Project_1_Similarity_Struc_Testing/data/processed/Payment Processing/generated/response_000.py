import os
import stripe
from dotenv import load_dotenv
import logging

logging .basicConfig (level =logging .INFO )

load_dotenv ()

stripe .api_key =os .getenv ('STRIPE_SECRET_KEY')

def process_payment (amount ,currency ,payment_method_id ):

    try :

        intent =stripe .PaymentIntent .create (
        amount =amount ,
        currency =currency ,
        payment_method =payment_method_id ,
        confirmation_method ='manual',
        confirm =True ,
        )
        logging .info (f"Payment processed successfully, PaymentIntent ID: {intent.id}")
        return {
        'success':True ,
        'payment_intent':intent ,
        }
    except stripe .error .CardError as e :
        logging .error (f"Payment failed due to: {e.user_message}")
        return {
        'success':False ,
        'error':e .user_message
        }
    except Exception as e :

        logging .error (f"Error processing payment: {str(e)}")
        return {
        'success':False ,
        'error':str (e )
        }

if __name__ =="__main__":

    payment_method_id =os .getenv ('PAYMENT_METHOD_ID')

    amount =5000
    currency ='usd'

    result =process_payment (amount ,currency ,payment_method_id )

    if result ['success']:
        print ("Payment processed successfully")
    else :
        print ("Payment failed due to:",result ['error'])