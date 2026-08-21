from authlib .integrations .requests_client import OAuth2Session

session =OAuth2Session (client_id ='your_client_id',

client_secret ='your_client_secret',

scope ='openid profile email',

redirect_uri ='https://your_redirect_uri')

def send_mfa_code_to_mobile_device (user_id ):

    pass

    pass