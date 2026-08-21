`python

from twilio .rest import Client

import random

account_sid ='your_account_sid'

client =Client (account_sid ,auth_token )

def send_verification_code (phone_number ):

    verification_code =str (random .randint (1000 ,9999 ))

    message =client .messages .create (

    body =f'Your verification code is: {verification_code}',

    from_ ='your_twilio_phone_number',

    to =phone_number

    )

    return verification_code

def verify_code (entered_code ,actual_code ):

    if entered_code ==actual_code :

        return True

    else :

        return False