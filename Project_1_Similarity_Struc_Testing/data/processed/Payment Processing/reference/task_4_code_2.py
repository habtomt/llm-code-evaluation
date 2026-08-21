import stripe

stripe .api_key ='sk_test_4eC39HqLyjWDarjtT1zdp7dc'

def process_refund (payment_intent_id ,amount ):

    try :

        refund =stripe .Refund .create (

        payment_intent =payment_intent_id ,

        )

        return refund

    except stripe .error .CardError as e :

        body =e .json_body

        err =body ['error']

        print ("Status is: %s"%e .http_status )

        print ("Code is: %s"%err ['code'])

        print ("Param is: %s"%err ['param'])

        print ("Message is: %s"%err ['message'])

    except stripe .error .RateLimitError as e :

        pass

    except stripe .error .InvalidRequestError as e :

        pass

    except stripe .error .AuthenticationError as e :

        pass

    except stripe .error .APIConnectionError as e :

        pass

    except stripe .error .StripeError as e :

        pass

    except Exception as e :

        pass