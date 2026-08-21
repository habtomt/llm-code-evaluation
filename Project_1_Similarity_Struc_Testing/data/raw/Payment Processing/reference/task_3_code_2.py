import stripe

stripe.api_key = 'your_secret_key'

payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency='usd',
    payment_method_types=['card'],
    receipt_email='jenny.rosen@example.com',
    confirm=True,
    confirmation_method='manual'
)

print(payment_intent)