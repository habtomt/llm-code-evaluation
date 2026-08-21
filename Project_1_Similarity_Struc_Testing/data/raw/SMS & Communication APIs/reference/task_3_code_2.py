`python

# Install Twilio package using pip if not already installed: 

# pip install twilio



from twilio.rest import Client



# Your Twilio account SID and auth token

account_sid = 'your_account_sid'

auth_token = 'your_auth_token'



client = Client(account_sid, auth_token)



# Function to send SMS notification to the customer

def send_sms_notification(customer_number, message):

    try:

        message = client.messages.create(

            body=message,

            from_='your_twilio_number',

            to=customer_number

        )

        print(f"SMS sent to {customer_number}: {message.sid}")

    except Exception as e:

        print(f"Failed to send SMS to {customer_number}: {str(e)}")



# Example usage

customer_number = '+1234567890'  # customer's phone number

send_sms_notification(customer_number, message)