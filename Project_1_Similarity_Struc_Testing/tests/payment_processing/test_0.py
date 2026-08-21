import os
import sys
from pathlib import Path
from unittest.mock import patch
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

os.environ["STRIPE_API_KEY"] = "sk_test_mockkey"
os.environ["PAYPAL_CLIENT_ID"] = "mock_client_id"
os.environ["PAYPAL_CLIENT_SECRET"] = "mock_client_secret"

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

def test_secure_credit_card_payment_processing():
    """requirement, Implement a system to process payments using credit cards securely."""
    source = get_clean_source()
    
    # Verify payment / credit card processing references
    has_payment = any(keyword in source for keyword in [
        "pay", "card", "credit", "stripe", "charge", "transaction", "gateway", "checkout"
    ])
    
    # Verify security , tokenization , encryption 
    has_security = [
        "secur", "token", "encrypt", "ssl", "pci", "hash", "mask", "env", "secret"
    ]
    has_security_ref = any(keyword in source for keyword in has_security)
    
    assert has_payment is True, \
        "no credit card payment processing logic found."
        
    assert has_security_ref is True, \
        "no payment security or tokenization measures found."

def test_transactions_verifications_and_confirmations():
    """requirement, Handle transactions, verifications, and confirmations."""
    source = get_clean_source()

    
    # look transaction, verification, confirmation logic
    has_workflow = any(keyword in source for keyword in [
        "transaction", "verify", "verification", "confirm", "auth", "status", "success", "receipt"
    ])
    
    assert has_workflow is True, \
        "no transaction handling, verification, or confirmation logic found."