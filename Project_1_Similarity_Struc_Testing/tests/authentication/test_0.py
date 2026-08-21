import re
import smtplib
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
import flask
import pytest

#root directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

#   move test execution to temporary folder and create the instance folder there
TEST_DIR = tempfile.mkdtemp()
os.chdir(TEST_DIR)
os.makedirs("instance", exist_ok=True)

smtplib.SMTP = MagicMock()
smtplib.SMTP_SSL = MagicMock()

def shim_before_first_request(self, func):
    
    return func

flask.Flask.before_first_request = shim_before_first_request

from target_app import User, app, db, mail


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["MAIL_SUPPRESS_SEND"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
def _smart_post(client, route, payload):
    #Try standard  form data first try json if rejected
    res = client.post(route, data=payload, follow_redirects=True)
    if res.status_code in (415, 400):
        res = client.post(route, json=payload, follow_redirects=True)
    return res


def test_signup_secure_storage(client):
    #"""requirement 1 and 2 signup system + secure database storage""
    test_email = "secure_test@example.com"
    test_password = "MySecretPassword123"

    response = _smart_post(
        client, "/signup", {"email": test_email, "password": test_password}
    )

    assert response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        assert user is not None, "User was not saved to the database."
        assert (
            user.password != test_password
        ), "SECURITY FAIL: Password stored in plaintext!"


def test_email_verification_flow(client):
    #"r requirement 3 include email verification to confirm the address
    test_email = "verify_me@example.com"

    with mail.record_messages() as outbox:
        _smart_post(
            client,
            "/signup",
            {"email": test_email, "password": "AnotherPassword123"},
        )

        assert len(outbox) == 1, "No confirmation email was sent."
        sent_email = outbox[0]
        assert test_email in sent_email.recipients
        email_body = sent_email.body if sent_email.body else sent_email.html

    urls = re.findall(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        email_body,
    )
    assert len(urls) > 0, "No URL link found in the verification email."

    confirm_route = "/" + urls[0].split("/", 3)[-1]
    confirm_response = client.get(confirm_route, follow_redirects=True)
    assert confirm_response.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email=test_email).first()
        is_active = (
            getattr(user, "verified", None)
            or getattr(user, "is_verified", None)
            or getattr(user, "confirmed", None)
        )
        assert (
            is_active is True
        ), "User account not flagged as verified after clicking link."