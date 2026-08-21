import os
import re
import sys
import smtplib
from pathlib import Path
from unittest.mock import MagicMock
import flask
import pytest

# root folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

smtplib.SMTP = MagicMock()
smtplib.SMTP_SSL = MagicMock()

try:
    import twilio.rest
    twilio.rest.Client = MagicMock()
except ImportError:
    pass

#  inject dummy Auth0/thirdparty keys
os.environ["AUTH0_DOMAIN"] = "dummy-tenant.auth0.com"
os.environ["AUTH0_CLIENT_ID"] = "dummy_client_id"
os.environ["AUTH0_CLIENT_SECRET"] = "dummy_client_secret"
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
except ImportError:
    APP_EXISTS = False
    app = None

try:
    from target_app import db, User
    DB_EXISTS = True
except ImportError:
    DB_EXISTS = False
    db = None
    User = None

try:
    from target_app import mail
except ImportError:
    mail = None


@pytest.fixture
def client():
    #setup isolated test env if the app exists"
    if not APP_EXISTS:
        yield None
        return

    app.config["TESTING"] = True
    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["MAIL_SUPPRESS_SEND"] = True

    with app.test_client() as test_client:
        with app.app_context():
            if DB_EXISTS:
                db.create_all()
            yield test_client
            if DB_EXISTS:
                db.session.remove()
                db.drop_all()


def _smart_post(client, route, payload):
    res = client.post(route, data=payload, follow_redirects=True)
    if res.status_code in (415, 400, 404):
        res = client.post(route, json=payload, follow_redirects=True)
    return res


def extract_mfa_code(user_email):
    if not DB_EXISTS: return None
    with app.app_context():
        user = User.query.filter_by(email=user_email).first()
        if user:
            totp_secret = getattr(user, "mfa_secret", getattr(user, "totp_secret", getattr(user, "secret", None)))
            if totp_secret:
                try:
                    import pyotp
                    return pyotp.TOTP(totp_secret).now()
                except ImportError:
                    pass

    if mail:
        with mail.record_messages() as outbox:
            if len(outbox) > 0:
                body = outbox[0].body or outbox[0].html
                match = re.search(r'\b\d{6}\b', body)
                if match: return match.group(0)
    return None


def test_mfa_enforcement(client):
    #"" Requirement is the system must require a second factor after password entry"""
    assert APP_EXISTS is True, "no functional web application found"
    
    # uUse llms dict if no db otherwise use standard signup
    if not DB_EXISTS:
        test_email = "user@example.com"
        test_password = "securepassword"
    else:
        test_email = "mfa_user@example.com"
        test_password = "SecurePassword123!"
        _smart_post(client, "/signup", {"email": test_email, "password": test_password})
        
    res = _smart_post(client, "/login", {"email": test_email, "password": test_password})
    
    html_text = res.get_data(as_text=True).lower()
    # otp to the keyword search
    mfa_keywords = ["mfa", "2fa", "two-factor", "code", "verify", "token", "authenticator", "auth0", "otp"]
    keyword_found = any(keyword in html_text for keyword in mfa_keywords)
    
    is_redirect = res.status_code in (301, 302)
    
    assert (keyword_found or is_redirect) is True, "system didnt prompt for MFA or redirect"


def test_mfa_completion(client):
    #"requiremnt entering the correct second factor completes identity verification
    assert APP_EXISTS is True, "no functional web application found"

    if not DB_EXISTS:
        # Bypass DB check and generate PyOTP directly from the LLM's dict
        test_email = "user@example.com"
        test_password = "securepassword"
        _smart_post(client, "/login", {"email": test_email, "password": test_password})
        
        import target_app
        import pyotp
        totp_secret = target_app.users[test_email]["otp_secret"]
        mfa_code = pyotp.TOTP(totp_secret).now()
    else:
        # Standard DB flow
        test_email = "mfa_verify@example.com"
        test_password = "SecurePassword123!"
        _smart_post(client, "/signup", {"email": test_email, "password": test_password})
        _smart_post(client, "/login", {"email": test_email, "password": test_password})
        mfa_code = extract_mfa_code(test_email)
        
    assert mfa_code is not None, "could not locate generated MFA code"

    # Added "otp" payload
    mfa_payloads = [{"code": mfa_code}, {"token": mfa_code}, {"mfa_code": mfa_code}, {"totp": mfa_code}, {"otp": mfa_code}]
    mfa_routes = ["/mfa", "/verify", "/login/mfa", "/2fa", "/verify_mfa"]
    
    success = False
    for route in mfa_routes:
        for payload in mfa_payloads:
            res = _smart_post(client, route, payload)
            html_lower = res.get_data(as_text=True).lower()
            if res.status_code in (200, 302) and "invalid" not in html_lower:
                success = True
                break
        if success: break

    assert success is True, "not successfully verify the generated MFA code"