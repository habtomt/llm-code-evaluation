from functools import wraps
from flask import Flask ,request ,jsonify
from authlib .integrations .flask_client import OAuth
from okta import UsersClient
from okta .models .user import User
from okta .models .app_linked_object import AppLinkedObject
from okta .models .role import Role

app =Flask (__name__ )
app .secret_key ='your_secret_key'

oauth =OAuth (app )
okta =oauth .register (
name ='okta',
client_id ='your_client_id',
client_secret ='your_client_secret',
server_metadata_url ='https://your_okta_domain.okta.com/oauth2/default'
)

def requires_role (role ):
    def decorator (f ):
        @wraps (f )
        def decorated_function (*args ,**kwargs ):

            auth_header =request .headers .get ('Authorization')
            if not auth_header :
                return jsonify ({'error':'Missing Authorization Header'}),401

            token =auth_header .split (" ")[1 ]if " "in auth_header else auth_header
            user_client =UsersClient ('https://your_okta_domain.okta.com',token )

            try :

                current_user =user_client .get_user ('me')

                if role in getattr (current_user .profile ,'roles',[]):
                    return f (*args ,**kwargs )
            except Exception as e :
                return jsonify ({'error':f'Authentication failed: {str(e)}'}),401

            return jsonify ({'error':'You do not have permission to access this resource'}),403
        return decorated_function
    return decorator

@app .route ('/admin')
@requires_role ('admin')
def admin_panel ():
    return 'Welcome to the admin panel'

@app .route ('/user')
@requires_role ('user')
def user_panel ():
    return 'Welcome to the user panel'

if __name__ =='__main__':
    app .run ()