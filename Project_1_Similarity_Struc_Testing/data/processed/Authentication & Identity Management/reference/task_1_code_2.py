from authlib .integrations .flask_client import OAuth
from flask import Flask ,redirect ,url_for ,session ,request ,jsonify
import os

app =Flask (__name__ )
app .secret_key =os .getenv ('SECRET_KEY')

oauth =OAuth (app )

auth0 =oauth .register (
'auth0',
client_id =os .getenv ('AUTH0_CLIENT_ID'),
client_secret =os .getenv ('AUTH0_CLIENT_SECRET'),
api_base_url ='https://'+os .getenv ('AUTH0_DOMAIN'),
access_token_url ='https://'+os .getenv ('AUTH0_DOMAIN')+'/oauth/token',
authorize_url ='https://'+os .getenv ('AUTH0_DOMAIN')+'/authorize',
client_kwargs ={
'scope':'openid profile email',
},
)

@app .route ('/callback')
def callback_handling ():
    auth0 .authorize_access_token ()
    resp =auth0 .get ('userinfo')
    userinfo =resp .json ()
    session ['jwt_payload']=userinfo
    session ['profile']={
    'user_id':userinfo ['sub'],
    'name':userinfo ['name'],
    'picture':userinfo ['picture']
    }
    return redirect ('/dashboard')

@app .route ('/login')
def login ():
    return auth0 .authorize_redirect (
    redirect_uri ='https://example.com/callback',
    audience ='https://'+os .getenv ('AUTH0_DOMAIN')+'/userinfo'
    )

@app .route ('/dashboard')
def dashboard ():

    return jsonify (
    jwt_payload =session .get ('jwt_payload'),
    profile =session .get ('profile')
    )

if __name__ =="__main__":
    app .run ()