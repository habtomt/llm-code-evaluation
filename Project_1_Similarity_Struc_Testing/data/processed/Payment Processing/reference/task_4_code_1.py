import stripe

def process_refund (payment_id ,amount ):
    stripe .api_key ='your_secret_key'
    payment =stripe .PaymentIntent .retrieve (payment_id )
    refund =stripe .Refund .create (
    payment_intent =payment_id ,
    amount =amount
    )
    return refund