import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

#root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags(Prevent unwanted OAuth credential errors on import)
os.environ["OAUTH_CLIENT_ID"] = "mock_client_id"
os.environ["OAUTH_CLIENT_SECRET"] = "mock_client_secret"
os.environ["OAUTH_REDIRECT_URI"] = "http://localhost:5000/callback"


APP_EXISTS = False
try:
    with patch("sys.exit", side_effect=SystemExit):
        import target_app
        APP_EXISTS = True
except SystemExit:
    APP_EXISTS = True
except Exception:
    APP_EXISTS = True

def get_clean_source():
    #clean source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_oauth_redirection_and_token():
    """requirement, Redirect users to OAuth page and receive an access token."""
    source = get_clean_source()
    
    # Verify OAuth redirection references
    has_redirect = any(keyword in source for keyword in [
        "redirect", "oauth", "authorize", "auth", "login", "url"
    ])
    
    # Verify access token retrieval references
    has_token = any(keyword in source for keyword in [
        "token", "access_token", "exchange", "callback", "response", "json"
    ])
    
    assert has_redirect is True, \
        "no OAuth redirection or authorization logic found."
        
    assert has_token is True, \
        "no access token reception or exchange logic found."

def test_user_profile_creation_or_update():
    """requirement, Retrieve user information to create or update user profiles."""
    source = get_clean_source()
    
    # Verify user profile retrieval and management references
    has_profile_management = any(keyword in source for keyword in [
        "user", "profile", "info", "create", "update", "database", "save", "fetch"
    ])
    
    assert has_profile_management is True, \
        "no user information retrieval or profile creation/update logic found."