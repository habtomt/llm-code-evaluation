from authlib.integrations.requests_client import OAuth2Session
from flask import Flask, redirect, url_for, session, request, jsonify
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

OAUTH2_CLIENT_ID = 'YOUR_CLIENT_ID'
OAUTH2_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
OAUTH2_REDIRECT_URI = 'YOUR_REDIRECT_URI'
OAUTH2_PROVIDER = 'provider_name'

# Configuration for the OAuth provider's API endpoints
# FIXED: Added the missing 'access_token_url' key string value mapping here
oauth_provider_configs = {
    'provider_name': {
        'authorize_url': 'PROVIDER_AUTHORIZE_URL',
        'access_token_url': 'PROVIDER_ACCESS_TOKEN_URL',
        'userinfo_url': 'PROVIDER_USERINFO_URL'
    }
}

@app.route('/login')
def login():
    # Best Practice: Initialize inside the route block execution context
    oauth = OAuth2Session(OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, redirect_uri=OAUTH2_REDIRECT_URI)
    
    # FIXED: Replaced undefined 'redirect_uri' name bound target with OAUTH2_REDIRECT_URI
    authorization_url, state = oauth.create_authorization_url(
        oauth_provider_configs[OAUTH2_PROVIDER]['authorize_url']
    )
    session['oauth_state'] = state # Save state to verify callback session security
    return redirect(authorization_url)

@app.route('/authorize')
def authorize():
    # Instantiate client session passing back state parameters for validation checks
    oauth = OAuth2Session(
        OAUTH2_CLIENT_ID, 
        OAUTH2_CLIENT_SECRET, 
        redirect_uri=OAUTH2_REDIRECT_URI, 
        state=session.get('oauth_state')
    )
    
    token = oauth.fetch_access_token(
        oauth_provider_configs[OAUTH2_PROVIDER]['access_token_url'],
        authorization_response=request.url
    )
    
    user_info = oauth.get(
        oauth_provider_configs[OAUTH2_PROVIDER]['userinfo_url']
    ).json()
    
    return jsonify(user_info)

if __name__ == '__main__':
    app.run()