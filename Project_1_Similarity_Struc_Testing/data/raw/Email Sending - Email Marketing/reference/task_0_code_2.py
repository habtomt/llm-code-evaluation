

import os

from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail, Email, Personalization, Content



# Set up SendGrid API key

sg_api_key = os.environ.get('SENDGRID_API_KEY')

sg_client = SendGridAPIClient(sg_api_key)



def send_promotional_email(email_list, customer_data):

    for email in email_list:

        message = Mail(

            from_email='your@email.com',

            to_emails=email,

            subject='Your Subject',

            html_content='<strong>Your HTML message here</strong>'

        )



        # Personalize email based on customer data

        personalization = Personalization()

        personalization.add_to(Email(email))

        personalization.add_dynamic_template_data(customer_data[email])  # assuming customer data is a dictionary

        message.add_personalization(personalization)



        # Send the email

        print(response.body)