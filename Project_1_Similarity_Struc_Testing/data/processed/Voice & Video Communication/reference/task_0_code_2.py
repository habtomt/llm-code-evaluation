`python

from twilio .rest import Client

account_sid ='your_account_sid'

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

room =client .video .rooms .create (unique_name ='my-room')