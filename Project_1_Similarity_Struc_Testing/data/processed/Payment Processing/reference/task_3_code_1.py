import stripe

stripe .api_key ='your_secret_api_key'

payment_intent =stripe .PaymentIntent .create (
amount =2000 ,
currency ='usd',
payment_method_types =['card'],
setup_future_usage ='off_session'
)

print (payment_intent )