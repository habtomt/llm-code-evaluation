`python

from twilio.rest import Client



account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)



# Replace with your own phone numbers

customer_number = '+15558675309'



message = client.messages.create(

    body='Your support inquiry has been resolved. Thank you for reaching out!',

    from_=twilio_number,

    to=customer_number

)



print(message.sid)