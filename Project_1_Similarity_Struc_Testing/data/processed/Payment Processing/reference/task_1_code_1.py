import stripe

stripe .api_key ='sk_test_4eC39HqLyjWDarjtT1zdp7dc'

customer =stripe .Customer .create (
email ='customer@example.com',
source ='tok_visa'
)

subscription =stripe .Subscription .create (
customer =customer .id ,
items =[
{
'price':'price_1JZ3q2BbCY3dNRbc'
}
]
)

stripe .Subscription .modify (
subscription .id ,
items =[
{
'id':subscription .items .data [0 ].id ,
'price':'price_1JZ3q2BbCY3dNRbc'
}
]
)

stripe .Subscription .delete (subscription .id )