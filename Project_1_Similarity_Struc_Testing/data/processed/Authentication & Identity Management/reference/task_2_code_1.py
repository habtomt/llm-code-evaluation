from flask import Flask ,redirect ,url_for ,session ,request
from flask_oauthlib .client import OAuth

app =Flask (__name__ )
app .secret_key ='development'
oauth =OAuth (app )

okta =oauth .remote_app (
'okta',
consumer_key ='YOUR_OKTA_CLIENT_ID',
consumer_secret ='YOUR_OKTA_CLIENT_SECRET',
request_token_params ={
'response_type':'code'
},
base_url ='https://dev-1234.okta.com',
request_token_url =None ,
access_token_method ='POST',
access_token_url ='https://dev-1234.okta.com/oauth2/default/v1/token',
authorize_url ='https://dev-1234.okta.com/oauth2/default/v1/authorize'
)

@app .route ('/login')
def login ():
    return okta .authorize (callback =url_for ('authorized',_external =True ))

@app .route ('/login/authorized')
def authorized ():
    resp =okta .authorized_response ()
    if resp is None or isinstance (resp ,Exception ):
        return 'Access denied: reason={} error={}'.format (
        request .args .get ('error_reason','Unknown'),
        request .args .get ('error_description','No details provided')
        )

    if isinstance (resp ,dict ):
        session ['okta_token']=(resp ['access_token'],'')
        user_info =okta .get ('userinfo').data
        return 'Logged in as: '+user_info .get ('name','Unknown User')

    return 'Failed to process authorization payload mapping.'

@okta .tokengetter
def get_okta_oauth_token ():
    return session .get ('okta_token')

if __name__ =='__main__':
    app .run ()