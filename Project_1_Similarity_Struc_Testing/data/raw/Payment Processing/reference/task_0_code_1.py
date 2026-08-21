import stripe

# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

# Token is created using Checkout or Elements!
# Get the payment token ID submitted by the form:
token = request.form['stripeToken']

# Charge the user's card:
charge = stripe.Charge.create(
    amount=1000,
    currency='usd',
    description='Example charge',
    source=token,
)