`python

import os

from twilio.rest import Client



account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)



def send_shipment_update(customer_number, order_status, tracking_number):

    message = client.messages.create(

        body=f"Hello! Your order has been {order_status}. Your tracking number is: {tracking_number}",

        from_='+1234567890',  # replace with your Twilio number

    )

    print(f"SMS sent to {customer_number}: {message.sid}")



# Example usage

customer_number = '+1234567890'  # replace with customer's phone number

order_status = 'shipped'  # replace with actual order status

send_shipment_update(customer_number, order_status, tracking_number)