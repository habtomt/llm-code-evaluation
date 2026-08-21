`python

from twilio.rest import Client



# Your Twilio Account SID and Auth Token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'

client = Client(account_sid, auth_token)



room = client.video.rooms.create(unique_name='telemedicine_room')



# Generate a video token for the healthcare provider

provider_token = client.tokens.create(identity='healthcare_provider', ttl=3600, video_grant={

    'room': room.sid

})



# Generate a video token for the patient

patient_token = client.tokens.create(identity='patient', ttl=3600, video_grant={

    'room': room.sid

})



# Your appointment scheduling and medical record sharing code goes here