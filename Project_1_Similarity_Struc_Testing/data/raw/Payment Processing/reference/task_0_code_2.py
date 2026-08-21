import stripe

# Set the API key
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

# Process a payment
def process_payment(amount, currency, card_number, exp_month, exp_year, cvc):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
            payment_method_data={
                'type': 'card',
                'card': {
                    'number': card_number,
                    'exp_month': exp_month,
                    'exp_year': exp_year,
                    'cvc': cvc,
                },
            },
            confirm=True,
            automatic_payment_methods={'enabled': True, 'allow_redirects': 'never'}
        )
        return "Payment processed successfully"
    except stripe.error.CardError as e:
        # Handle card processing errors
        return f"Card error: {e.error.message}"
    except stripe.error.InvalidRequestError as e:
        # Handle invalid payment requests
        return f"Invalid request error: {e.error.message}"
    except Exception as e:
        # Handle other exceptions
        return f"Error occurred: {str(e)}"

# Verify a payment
def verify_payment(payment_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_id)
        return f"Payment {payment_id} is {payment_intent.status}"
    except stripe.error.InvalidRequestError as e:
        # Handle invalid payment requests
        return f"Invalid request error: {e.error.message}"
    except Exception as e:
        # Handle other exceptions
        return f"Error occurred: {str(e)}"