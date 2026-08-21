# Import the stripe library
import stripe

# Set the API key for the Stripe API
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

# Create a new customer
customer = stripe.Customer.create(
    email='customer@example.com',
    source='tok_visa'  # Token representing the user's credit card
)

# Create a subscription for the customer
subscription = stripe.Subscription.create(
    customer=customer.id,
    items=[
        {
            'price': 'price_1JZ3q2BbCY3dNRbc'
        }
    ]
)

# Update the subscription schedule for recurring payments
stripe.Subscription.modify(
    subscription.id,
    items=[
        {
            'id': subscription.items.data[0].id,
            'price': 'price_1JZ3q2BbCY3dNRbc'
        }
    ]
)

# Cancel the subscription
stripe.Subscription.delete(subscription.id)