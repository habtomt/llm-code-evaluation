stripe .api_key ="sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def process_mobile_payment (amount ,currency ,mobile_wallet_info ):

    payment_intent =stripe .PaymentIntent .create (

    currency =currency ,

    payment_method_types =["card","mobile_wallet"],

    mobile_wallet =mobile_wallet_info

    )

    return payment_intent