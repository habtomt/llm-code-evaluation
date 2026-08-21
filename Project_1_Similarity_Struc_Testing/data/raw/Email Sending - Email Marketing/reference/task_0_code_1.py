import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, Substitution

API_KEY = os.environ.get('SENDGRID_API_KEY')
sg = SendGridAPIClient(API_KEY)

subscribers = [
    {"email": "subscriber1@example.com", "name": "John Doe", "timezone": "EST"},
    {"email": "subscriber2@example.com", "name": "Jane Smith", "timezone": "PST"}
]

template_id = "your_template_id_here"

for subscriber in subscribers:
    message = Mail(from_email="your@example.com", to_emails=subscriber["email"])
    message.template_id = template_id
    message.dynamic_template_data = {
        "name": subscriber["name"],
        "timezone": subscriber["timezone"],
        # Add other personalized fields as needed
    }
    sg.send(message)