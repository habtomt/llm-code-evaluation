from flask import Flask ,request ,redirect ,url_for ,session
from authlib .integrations .flask_client import OAuth
from authlib .common .security import generate_token

app =Flask (__name__ )
app .secret_key ='your secret key'

oauth =OAuth (app )
auth0 =oauth .register (
name ='auth0',
server_metadata_url ='https://your-auth0-domain/.well-known/openid-configuration',
client_id ='your-client-id',
client_secret ='your-client-secret',
)

def token_is_valid (token ):

    return True

@app .route ('/password/reset/request',methods =['POST'])
def password_reset_request ():
    email =request .form ['email']

    reset_token =generate_token ()

    return 'Reset link sent to your email'

@app .route ('/password/reset/<token>',methods =['GET'])
def password_reset_verify (token ):

    if token_is_valid (token ):
        session ['reset_token']=token
        return redirect (url_for ('password_reset_form'))
    else :
        return 'Invalid or expired reset link'

@app .route ('/password/reset',methods =['GET','POST'])
def password_reset_form ():
    if request .method =='GET':

        return 'Password reset form'
    else :

        reset_token =session .get ('reset_token')
        if reset_token and token_is_valid (reset_token ):

            return 'Password updated successfully'
        else :
            return 'Invalid or expired reset link'

if __name__ =='__main__':
    app .run ()