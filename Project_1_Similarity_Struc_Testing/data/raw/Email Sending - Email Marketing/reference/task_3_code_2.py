

import os

from sendgrid import SendGridAPIClient



def send_confirmation_email(email):

    message = Mail(

        to_emails=email,

        subject='Newsletter Subscription Confirmation',

        html_content='<p>Thank you for subscribing to our newsletter!</p><p>Click <a href="http://yourdomain.com/manage_preferences">here</a> to manage your email preferences.</p>'

    )

    try:

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

        response = sg.send(message)

        print(response.status_code)

        print(response.body)

        print(response.headers)

    except Exception as e:

        print(e.message)



# Call send_confirmation_email function with the subscriber's email

send_confirmation_email('subscriber@example.com')