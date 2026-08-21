`python

from twilio .rest import Client

from twilio .jwt .access_token import AccessToken

from twilio .jwt .access_token .grants import VideoGrant ,VoiceGrant

from twilio .base .exceptions import TwilioException

account_sid ='your_account_sid'

auth_token ='your_auth_token'

client =Client (account_sid ,auth_token )

def generate_token (identity ):

    token =AccessToken (account_sid ,api_key ,api_secret ,identity =identity )

    token .add_grant (VideoGrant (room ='gaming_room'))

    token .add_grant (VoiceGrant ())

    return token .to_jwt ()

    try :

        token =generate_token (identity )

        print (token )

    except TwilioException as e :

        print (f"Error joining voice chat: {e}")

join_voice_chat ('player2','gaming_room')