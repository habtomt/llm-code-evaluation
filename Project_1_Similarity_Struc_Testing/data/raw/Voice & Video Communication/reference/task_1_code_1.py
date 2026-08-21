`python

from twilio.rest import Client

from twilio.jwt.access_token import AccessToken

from twilio.jwt.access_token.grants import VideoGrant, VoiceGrant

from twilio.base.exceptions import TwilioException



# Your Twilio account SID and auth token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'



# Initialize the Twilio client

client = Client(account_sid, auth_token)



# Generate an access token for the user

def generate_token(identity):

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    token.add_grant(VideoGrant(room='gaming_room'))

    token.add_grant(VoiceGrant())

    return token.to_jwt()



# Join a room for voice chat

    try:

        token = generate_token(identity)

        print(token)



        # Connect to the voice chat room using the token

        # Insert code to connect to Twilio Voice SDK for low-latency communication

        # Add functionalities for push-to-talk and background noise suppression

    except TwilioException as e:

        print(f"Error joining voice chat: {e}")



# Example usage

join_voice_chat('player2', 'gaming_room')