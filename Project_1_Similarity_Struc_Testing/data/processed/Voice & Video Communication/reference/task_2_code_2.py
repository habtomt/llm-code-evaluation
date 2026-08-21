`python

from twilio .rest import Client

account_sid ='your_account_sid'

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

call =client .calls .create (

url ='http://demo.twilio.com/docs/voice.xml',

to ='customer_phone_number',

from_ ='twilio_phone_number'

)

call .update (method ='POST',status_callback_event =['completed'],status_callback ='your_callback_url')

recordings =client .recordings .list (call_sid =call .sid )

for recording in recordings :

    analyze_voice (recording .uri )