`python

from twilio.rest import Client



# Your Twilio Account SID and Auth Token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'



# Send SMS to a list of subscribers

subscribers = ['subscriber1', 'subscriber2', 'subscriber3']

for subscriber in subscribers:

    message = client.messages.create(

        body='Special offer alert! Get 20% off on your next purchase. Use code: SPECIAL20',

        from_='your_twilio_number',

    )

    print(f"Message sent to {subscriber}: {message.sid}")