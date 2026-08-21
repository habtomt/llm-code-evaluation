`python

import os

from twilio .rest import Client

account_sid ='your_account_sid'

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

def send_shipment_update (customer_number ,order_status ,tracking_number ):

    message =client .messages .create (

    body =f"Hello! Your order has been {order_status}. Your tracking number is: {tracking_number}",

    from_ ='+1234567890',

    )

    print (f"SMS sent to {customer_number}: {message.sid}")

customer_number ='+1234567890'

order_status ='shipped'

send_shipment_update (customer_number ,order_status ,tracking_number )