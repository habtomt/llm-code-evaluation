`python

from twilio.rest import Client



# Your Twilio account SID and auth token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)



# Create a new Room

room = client.video.rooms.create(unique_name='my-room')