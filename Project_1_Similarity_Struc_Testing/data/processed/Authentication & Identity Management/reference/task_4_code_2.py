from authlib .integrations .flask_client import OAuth
from flask import Flask ,jsonify ,request
from functools import wraps

app =Flask (__name__ )
app .secret_key ='your-secret-key'
oauth =OAuth (app )

auth0 =oauth .register (
'auth0',
client_id ='your-client-id',
client_secret ='your-client-secret',
api_base_url ='https://your-domain.auth0.com',
access_token_url ='https://your-domain.auth0.com/oauth/token',
authorize_url ='https://your-domain.auth0.com/authorize',
client_kwargs ={
'scope':'openid profile email',
},
)

def requires_role (allowed_roles ):
    def decorator (f ):
        @wraps (f )
        def decorated_function (*args ,**kwargs ):
            if 'access_token'not in request .cookies :
                return jsonify ({'message':'Missing access token'}),401

            access_token =request .cookies ['access_token']
            userinfo =auth0 .get ('userinfo').json ()
            user_roles =userinfo .get ('https://your-domain.auth0.com/roles',[])

            for role in allowed_roles :
                if role in user_roles :
                    return f (*args ,**kwargs )

            return jsonify ({'message':'Insufficient permissions'}),403
        return decorated_function
    return decorator

@app .route ('/admin')
@requires_role (['admin'])
def admin_dashboard ():
    return jsonify ({'message':'Welcome to the admin dashboard'})

@app .route ('/user')
@requires_role (['user'])
def user_dashboard ():
    return jsonify ({'message':'Welcome to the user dashboard'})

if __name__ =='__main__':
    app .run ()