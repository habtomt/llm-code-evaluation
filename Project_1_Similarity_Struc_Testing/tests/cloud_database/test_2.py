import os
import sys
from pathlib import Path
import pytest

#root folder 
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

# env gags
os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/dev/null"


APP_EXISTS = False
try:
    import target_app
    APP_EXISTS = True
except Exception:
    pass

def get_clean_source():
    #clean source code for whitespace
    try:
        with open("target_app.py", "r", encoding="utf-8") as f:
            raw_source = f.read().lower()
            return raw_source.replace(" ", "").replace("\n", "").replace('"', '').replace("'", "")
    except Exception:
        return ""

def test_auth_and_rbac():
    """requirement, Set up authentication and role-based access controls (RBAC)"""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # 1. Look for Authentication logic (passwords, IAM auth, credentials)
    has_auth = any(keyword in source for keyword in [
        "auth", "password", "iam", "credential", "login", "user"
    ])
    
    # 2. Look for Role-Based Access Control logic (Roles, Grants, Policies)
    has_rbac = any(keyword in source for keyword in [
        "role", "grant", "policy", "permission", "rbac", "revoke", "group"
    ])
    
    assert has_auth is True, \
        "no authentication configuration or logic found."
        
    assert has_rbac is True, \
        "no role-Based Access Control logic found"

def test_encryption_and_logging():
    """requirement, Encryption for data in transit/rest, and audit logging."""
    assert APP_EXISTS is True, "code failed to compile or crashed on initialization"
    
    source = get_clean_source()
    
    # look for Encryption
    has_encryption = any(keyword in source for keyword in [
        "encrypt", "kms", "ssl", "tls", "cipher", "transit", "rest", "certificate"
    ])
    
    #Look for Audit logging
    has_logging = any(keyword in source for keyword in [
        "audit", "log", "trail", "cloudwatch", "export", "monitor"
    ])
    
    assert has_encryption is True, \
        "no encryption configuration (at rest or in transit) found."
        
    assert has_logging is True, \
        "no audit logging configuration found."