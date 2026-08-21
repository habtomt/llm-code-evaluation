



stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

# Create a customer

customer = stripe.Customer.create(

  email='customer@example.com',

)



# Create a subscription

subscription = stripe.Subscription.create(

  customer=customer.id,

  items=[

    {

      'price': 'price_1HKYxCBE5jM8B7dcz49dIodq',

    },

  ]

)



# Update subscription to set up automatic payments

stripe.Subscription.modify(

  subscription.id,

  payment_behavior='default_incomplete',

)



# Manage and cancel subscription

stripe.Subscription.delete(

  subscription.id,

  invoice_now=True,

)