

import stripe



def process_mobile_payment(amount, currency, description, source, customer_email):

    stripe.api_key = 'your_secret_key'



    try:

        payment_intent = stripe.PaymentIntent.create(

            amount=amount,

            description=description,

            payment_method=source,

            confirmation_method='manual',

            confirm=True,

        )

        return payment_intent

    except stripe.error.CardError as e:

        error = e.error.message

        return error