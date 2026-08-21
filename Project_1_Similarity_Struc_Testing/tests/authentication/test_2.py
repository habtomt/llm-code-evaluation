import os
import sys
from pathlib import Path
import flask
import pytest

#        root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["GOOGLE_CLIENT_ID"] = "dummy_google_id"
os.environ["GOOGLE_CLIENT_SECRET"] = "dummy_google_secret"
os.environ["GITHUB_CLIENT_ID"] = "dummy_github_id"
os.environ["GITHUB_CLIENT_SECRET"] = "dummy_github_secret"
os.environ["FACEBOOK_CLIENT_ID"] = "dummy_facebook_id"
os.environ["FACEBOOK_CLIENT_SECRET"] = "dummy_facebook_secret"
os.environ["OAUTH_CLIENT_ID"] = "dummy_oauth_id"
os.environ["OAUTH_CLIENT_SECRET"] = "dummy_oauth_secret"
os.environ["SECRET_KEY"] = "dummy_secret"

def shim_before_first_request(self, func):
    self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with self.app_context():
        func()
    return func

flask.Flask.before_first_request = shim_before_first_request

try:
    from target_app import app
    APP_EXISTS = True
except Exception:  # catches runtimeError or  syntaxerror
    APP_EXISTS = False
    app = None

try:
    from target_app import db, User
    DB_EXISTS = True
except Exception:  
    DB_EXISTS = False
    db = None
    User = None


@pytest.fixture
def client():
    
    if not APP_EXISTS:
        yield None
        return

    app.config["TESTING"] = True
    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.test_client() as test_client:
        with app.app_context():
            if DB_EXISTS:
                db.create_all()
            yield test_client
            if DB_EXISTS:
                db.session.remove()
                db.drop_all()


def test_oauth_initiation(client):
    """     requirement iss Implement OAuth 2.0 or a similar protocol to handle authentication"""
    assert APP_EXISTS is True, "  no functional web application found."
    
    oauth_routes = [
        "/login", "/login/google", "/login/github", "/login/facebook", 
        "/auth", "/auth/login", "/auth/google", "/oauth/login", "/authorize"
    ]
    
    found_oauth_redirect = False
    
    for route in oauth_routes:
        res = client.get(route, follow_redirects=False)
        
        #       c Check if the route returns redirect to an external provider
        if res.status_code in (301, 302, 307):
            location = res.headers.get("Location", "").lower()
            
            #look for standard OAuth 2.0 url   parameters
            is_oauth_url = "client_id=" in location and ("redirect_uri=" in location or "response_type=" in location)
            
            # look for known provider domains
            known_providers = [
                "google.com/o/oauth2", 
                "github.com/login/oauth", 
                "facebook.com/dialog/oauth", 
                "auth0.com/authorize"
            ]
            
            if is_oauth_url or any(provider in location for provider in known_providers):
                found_oauth_redirect = True
                break
                
    assert found_oauth_redirect is True, "system didnot initiate an OAuth 2.0 authorization redirect"


def test_oauth_profile_storage(client):
    #"""rrequirement retrieve and store only necessary profile information"""
    assert APP_EXISTS is True, "No functional web application found."
    assert DB_EXISTS is True, "code doesnt implement required local database models for testing."

    with app.app_context():
        # Iinspect user model schema 
        user_columns = [col.name.lower() for col in User.__table__.columns]
        
        oauth_indicators = [
            "social_id", "oauth_id", "provider", "provider_id", 
            "google_id", "github_id", "facebook_id", "avatar"
        ]
        
        
        has_oauth_fields = any(indicator in user_columns for indicator in oauth_indicators)
        
        
        password_col = next((col for col in User.__table__.columns if "password" in col.name.lower()), None)
        allows_null_password = password_col.nullable if password_col else True
        
        assert (has_oauth_fields or allows_null_password) is True, \
            "user model is not properly structured to store oauth profile information"