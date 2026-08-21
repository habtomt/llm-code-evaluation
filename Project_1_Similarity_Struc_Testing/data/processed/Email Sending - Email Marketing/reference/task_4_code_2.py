import os
from sendgrid import SendGridAPIClient
from sendgrid .helpers .mail import Mail

def send_event_invitation (emails ,event_name ,event_date ):
    try :
        message =Mail (
        from_email ='your_email@example.com',
        to_emails =emails ,
        subject =f'You are invited to {event_name}!',
        )
        sg =SendGridAPIClient (os .environ .get ('SENDGRID_API_KEY'))
        response =sg .send (message )
        print ('Invitations sent successfully!')
    except Exception as e :
        print (f'Error sending invitations: {e}')

send_event_invitation (['recipient1@example.com','recipient2@example.com'],'Awesome Event','2023-12-31')