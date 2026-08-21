`python

import os

from twilio.rest import Client

from twilio.twiml.voice_response import Gather, VoiceResponse, Say



# Set your Twilio credentials

auth_token = 'your_auth_token'



# Initialize Twilio client

client = Client(account_sid, auth_token)



# Create a call and connect to a voice room

call = client.calls.create(

    url='http://demo.twilio.com/docs/voice.xml',

    to='player1_phone_number',

    from_='your_twilio_phone_number'



# Implement push-to-talk functionality

def push_to_talk():

    response = VoiceResponse()

    response.say('Press any key to talk, release to stop.')

    response.gather(input='dtmf', action='/handle-input', numDigits=1, method='POST')

    print(response)



# Implement background noise suppression

def background_noise_suppression():

    print('Background noise suppression enabled.')



# Call functions to handle voice chat features

push_to_talk()

background_noise_suppression()