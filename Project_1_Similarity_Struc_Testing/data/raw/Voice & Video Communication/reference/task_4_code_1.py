`python

from twilio.jwt.access_token import AccessToken

from twilio.jwt.access_token.grants import VideoGrant, VoiceGrant

from twilio.rest import Client



# Your Twilio account SID and auth token

account_sid = 'your_account_SID'

auth_token = 'your_auth_token'



# Generate an access token with video grant

def generate_token(identity, room):

    token = AccessToken(account_sid, api_key, api_secret, identity=identity)

    token.add_grant(VideoGrant(room=room))

    token.add_grant(VoiceGrant())

    return token.to_jwt()



# Initialize Twilio client

client = Client(account_sid, auth_token)



# Schedule video call appointment

def schedule_video_call(provider, patient, scheduled_time):

    # Logic to schedule appointment

    pass

def share_medical_record(caller, receiver, record_url):

    # Logic to share medical record during video call

    pass