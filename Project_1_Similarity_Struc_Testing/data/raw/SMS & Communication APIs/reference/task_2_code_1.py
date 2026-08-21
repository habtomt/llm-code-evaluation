`python

from twilio.rest import Client



# Your Twilio Account SID and Auth Token

account_sid = 'your_account_sid'



# Create a list of subscribers

subscribers = ['subscriber1', 'subscriber2', 'subscriber3']



# Send promotional messages to the subscribers

for subscriber in subscribers:

    message = client.messages.create(

        body='Check out our special offer! Limited time only!',

        from_='your_twilio_number',

        to=subscriber

    )

    print(f"Message sent to {subscriber} with SID: {message.sid}")