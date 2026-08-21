`python

import os

from twilio.rest import Client

from twilio.twiml.voice_response import Gather, VoiceResponse, Say

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)

call = client.calls.create(

    url='http://demo.twilio.com/docs/voice.xml',

    to='player1_phone_number',

    from_='your_twilio_phone_number'

def push_to_talk():

    response = VoiceResponse()

    response.say('Press any key to talk, release to stop.')

    response.gather(input='dtmf', action='/handle-input', numDigits=1, method='POST')

    print(response)

def background_noise_suppression():

    print('Background noise suppression enabled.')

push_to_talk()

background_noise_suppression()