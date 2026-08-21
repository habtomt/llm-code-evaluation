`python

import os

from twilio.rest import Client

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

message = client.messages.create(

    body='Your appointment is coming up on 07/09/2023 at 2:30 PM',

    from_='your_twilio_number',

    to='customer_number'

print(message.sid)