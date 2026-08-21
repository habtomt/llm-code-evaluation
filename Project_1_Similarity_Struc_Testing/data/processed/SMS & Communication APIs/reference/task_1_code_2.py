`python

from twilio .rest import Client

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

message =client .messages
    .create (

    from_ ='your_twilio_number',

    to ='customer_phone_number'

    )

print (message .sid )