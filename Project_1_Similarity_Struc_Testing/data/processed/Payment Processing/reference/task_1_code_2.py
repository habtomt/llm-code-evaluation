stripe .api_key ='sk_test_4eC39HqLyjWDarjtT1zdp7dc'

customer =stripe .Customer .create (

email ='customer@example.com',

)

subscription =stripe .Subscription .create (

customer =customer .id ,

items =[

{

'price':'price_1HKYxCBE5jM8B7dcz49dIodq',

},

]

)

stripe .Subscription .modify (

subscription .id ,

payment_behavior ='default_incomplete',

)

stripe .Subscription .delete (

subscription .id ,

invoice_now =True ,

)