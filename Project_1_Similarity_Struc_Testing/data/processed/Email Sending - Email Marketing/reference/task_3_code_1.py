import sendgrid

from sendgrid .helpers .mail import *

def send_confirmation_email (email_address ):

    from_email =Email ("your@email.com")

    to_email =Email (email_address )

    subject ="Newsletter Subscription Confirmation"

    content =Content ("text/plain","Thanks for subscribing to our newsletter!")

    response =sg .client .mail .send .post (request_body =mail .get ())

def manage_email_preferences (email_address ):

    pass

email_address ="example@example.com"

send_confirmation_email (email_address )