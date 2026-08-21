`python

from twilio .rest import Client

account_sid ='your_account_sid'

subscribers =['subscriber1','subscriber2','subscriber3']

for subscriber in subscribers :

    message =client .messages .create (

    body ='Check out our special offer! Limited time only!',

    from_ ='your_twilio_number',

    to =subscriber

    )

    print (f"Message sent to {subscriber} with SID: {message.sid}")