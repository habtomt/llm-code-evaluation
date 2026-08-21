import stripe

stripe .api_key ='sk_test_4eC39HqLyjWDarjtT1zdp7dc'

token =request .form ['stripeToken']

charge =stripe .Charge .create (
amount =1000 ,
currency ='usd',
description ='Example charge',
source =token ,
)