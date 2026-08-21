

import sendgrid

from sendgrid.helpers.mail import *

import os



sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))



def send_abandoned_cart_email(user_email, cart_items, personalized_recommendations):

    message = Mail(

        from_email='noreply@example.com',

        to_emails=user_email,

        subject='We noticed you left something in your cart!',

        html_content=f'''

        <p>Dear valued customer,</p>

        <p>We noticed that you left the following items in your cart:</p>

        <ul>

        </ul>

        <ul>

            {", ".join(personalized_recommendations)}

        </ul>

        <p>We hope you will find these recommendations helpful and complete your purchase soon!</p>

        <p>Sincerely,<br>Your Online Store Team</p>

        '''

    )

    response = sg.send(message)

    print(response.status_code)

    print(response.body)

    print(response.headers)