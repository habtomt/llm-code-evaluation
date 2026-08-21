import requests
import json
from datetime import datetime ,timedelta
import base64

def send_password_reset_link (email ):
    reset_link ="http://example.com/reset_password?token={}".format (generate_reset_token (email ))

def generate_reset_token (email ):
    current_time =datetime .utcnow ()
    expiry_time =current_time +timedelta (hours =1 )
    token_payload ={
    "email":email ,
    "expiry_time":expiry_time .isoformat ()
    }
    token =base64 .b64encode (json .dumps (token_payload ).encode ()).decode ()
    return token

def validate_reset_token (token ):
    try :

        decoded_bytes =base64 .b64decode (token .encode ())
        token_payload =json .loads (decoded_bytes .decode ())

        expiry_time =datetime .fromisoformat (token_payload ['expiry_time'])

        if datetime .utcnow ()<=expiry_time :
            return True
    except Exception :

        return False

    return False

user_email ="example@example.com"
send_password_reset_link (user_email )

simulated_token =generate_reset_token (user_email )

if validate_reset_token (simulated_token ):

    print ("Valid token. Allowing password change.")
else :
    print ("Invalid token. Password reset link has expired.")