import os

from sendgrid import SendGridAPIClient

from sendgrid .helpers .mail import Mail ,Email ,Content

def send_welcome_email (email_address ):

    message =Mail (

    from_email =Email ('your_email@example.com','Your Name'),

    html_content ='<strong>Thank you for subscribing to our newsletter! Here is some valuable content to get you started...</strong>'

    )

    try :

        sg =SendGridAPIClient (os .environ .get ('SENDGRID_API_KEY'))

        response =sg .send (message )

        print (response .status_code )

        print (response .body )

        print (response .headers )

    except Exception as e :

        print (e .message )

send_welcome_email ('new_subscriber@example.com')