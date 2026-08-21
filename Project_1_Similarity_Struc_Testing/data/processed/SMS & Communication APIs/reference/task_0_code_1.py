`python

from twilio .rest import Client

account_sid ='Your_Account_SID'

twilio_phone_number ='Your_Twilio_Phone_Number'

def send_verification_code (phone_number ):

    verification_code =str (random .randint (1000 ,9999 ))

    client =Client (account_sid ,auth_token )

    message =client .messages .create (

    body =f'Your verification code is {verification_code}',

    from_ =twilio_phone_number ,

    to =phone_number

    )

    return verification_code

user_phone_number ='User_Phone_Number'

verification_code =send_verification_code (user_phone_number )

print (f'Verification code sent to {user_phone_number}: {verification_code}')