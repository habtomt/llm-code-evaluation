`python

from twilio .rest import Client

account_sid ='your_account_sid'

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

from_number ='your_twilio_phone_number'

to_number ='customer_phone_number'

message =client .messages .create (

body ='Your order has been shipped! Here is the tracking number: 12345',

from_ =from_number ,

to =to_number

)