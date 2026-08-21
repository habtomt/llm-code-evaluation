`python

from twilio.rest import Client

from twilio.jwt.access_token import AccessToken

from twilio.jwt.access_token.grants import VideoGrant

from twilio.twiml.voice_response import Dial, VoiceResponse



# Set up Twilio credentials

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)



# Create an access token

token = AccessToken(account_sid, api_key, api_secret, identity='user123')

# Add permissions to the access token

token.add_grant(video_grant)



# Return token to client

print(token.to_jwt())