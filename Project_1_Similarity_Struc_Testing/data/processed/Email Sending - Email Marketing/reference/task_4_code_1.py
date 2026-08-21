import sendgrid

from sendgrid .helpers .mail import Mail ,Email ,Content

sg =sendgrid .SendGridAPIClient (api_key ='YOUR_SENDGRID_API_KEY')

def send_event_invitation (invitees ,event_name ,event_date ):

    for invitee in invitees :

        to_email =Email (invitee )

        subject =f"You're Invited to {event_name}!"

        content =Content ("text/plain",f"Hey there! You are invited to {event_name} on {event_date}. Please RSVP to this email.")

        mail =Mail (from_email ,subject ,to_email ,content )

        response =sg .client .mail .send .post (request_body =mail .get ())

def send_reminder (invitees ,event_name ,reminder_date ):

    for invitee in invitees :

        from_email =Email ("your email@example.com")

        to_email =Email (invitee )

        subject =f"Reminder: {event_name} is coming up soon!"

        mail =Mail (from_email ,subject ,to_email ,content )

        response =sg .client .mail .send .post (request_body =mail .get ())