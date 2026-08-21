`python

from twilio.rest import Client



# Your Twilio Account SID and Auth Token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'



# Create a TwiML response for handling incoming voice call

twiml_response = """

<Response>

    <Say>Welcome to Virtual Customer Support. Please wait while we connect you to a support agent.</Say>

    <Dial>

        <Client>support_agent</Client>

    </Dial>

</Response>

"""



# Configure Twilio to use the TwiML response

call = client.calls.create(

    twiml=twiml_response,

    from_='your_twilio_phone_number'

)



print(call.sid)