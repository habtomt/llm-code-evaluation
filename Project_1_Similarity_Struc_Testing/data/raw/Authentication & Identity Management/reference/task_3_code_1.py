import requests
import json
from datetime import datetime, timedelta
import base64  # FIXED: Added missing import

# Function to send password reset link to user's email
def send_password_reset_link(email):
    reset_link = "http://example.com/reset_password?token={}".format(generate_reset_token(email))
    # Send email with password reset link

# Function to generate time-sensitive reset token
def generate_reset_token(email):
    current_time = datetime.utcnow()
    expiry_time = current_time + timedelta(hours=1)  # Set token expiry time
    token_payload = {
        "email": email,
        "expiry_time": expiry_time.isoformat()
    }
    token = base64.b64encode(json.dumps(token_payload).encode()).decode()
    return token

# Function to validate reset token and allow password change
def validate_reset_token(token):
    try:
        # FIXED: Added the missing token base64 decoding and JSON loading step
        decoded_bytes = base64.b64decode(token.encode())
        token_payload = json.loads(decoded_bytes.decode())
        
        expiry_time = datetime.fromisoformat(token_payload['expiry_time'])
        
        # FIXED: Simplified return block statement
        if datetime.utcnow() <= expiry_time:
            return True
    except Exception:
        # If decoding or parsing JSON payload parameters fails, treat token as invalid
        return False
        
    return False

# Example usage
user_email = "example@example.com"
send_password_reset_link(user_email)

# Simulation helper for testing example flow
simulated_token = generate_reset_token(user_email)

# When user follows the link from their email
if validate_reset_token(simulated_token):
    # Allow password change
    print("Valid token. Allowing password change.")
else:
    print("Invalid token. Password reset link has expired.")