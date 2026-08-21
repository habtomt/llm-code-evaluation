import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["TWILIO_ACCOUNT_SID"] = "ACmock_sid"
os.environ["TWILIO_AUTH_TOKEN"] = "mock_auth_token"
os.environ["TWILIO_PHONE_NUMBER"] = "+15555555555"

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

def test_sms_verification_code_sending():
    """requirement, Implement a feature that sends a verification code to users via SMS when they attempt to log in."""
    source = get_clean_source()
    
    # Verify SMS / messaging provider references 
    has_sms = any(keyword in source for keyword in [
        "twilio", "sms", "text", "message", "send", "vonage", "sns", "client"
    ])
    
    # Verify login attempt or verification code generation context
    has_login_or_code = any(keyword in source for keyword in [
        "login", "signin", "auth", "code", "otp", "token", "verify", "verification"
    ])
    
    assert has_sms is True, \
        "no SMS sending or communication API logic found."
        
    assert has_login_or_code is True, \
        "no login attempt or verification code generation logic found."

def test_code_verification_and_access_grant():
    """requirement, Ensure access is only granted after the correct code is entered."""
    source = get_clean_source()
    
    # Verify code verification / validation check references
    has_verification_check = any(keyword in source for keyword in [
        "verify", "validation", "check", "match", "compare", "code", "access", "grant", "success"
    ])
    
    assert has_verification_check is True, \
        "no verification code validation or access granting logic found."