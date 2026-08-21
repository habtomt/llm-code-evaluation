`python

from twilio .rest import Client

account_sid ='your_account_sid'

auth_token ='your_auth_token'

twiml_response ="""

<Response>

    <Say>Welcome to Virtual Customer Support. Please wait while we connect you to a support agent.</Say>

    <Dial>

        <Client>support_agent</Client>

    </Dial>

</Response>

"""

call =client .calls .create (

twiml =twiml_response ,

from_ ='your_twilio_phone_number'

)

print (call .sid )