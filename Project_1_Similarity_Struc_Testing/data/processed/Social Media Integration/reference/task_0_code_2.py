`python

import requests

def get_facebook_login_url (redirect_uri ,client_id ,scope ):

    base_url ="https://www.facebook.com/v9.0/dialog/oauth"

    params ={

    "client_id":client_id ,

    "redirect_uri":redirect_uri ,

    "scope":scope ,

    }

    query_params ="&".join ([f"{key}={value}"for key ,value in params .items ()])

    login_url =f"{base_url}?{query_params}"

    return login_url

def exchange_facebook_token (client_id ,client_secret ,redirect_uri ,code ):

    base_url ="https://graph.facebook.com/v9.0/oauth/access_token"

    params ={

    "client_id":client_id ,

    "client_secret":client_secret ,

    "redirect_uri":redirect_uri ,

    "code":code ,

    }

    response =requests .get (base_url ,params =params )

    access_token =response .json ().get ("access_token")

    return access_token

def get_facebook_user_info (access_token ,fields ="id,name,email"):

    base_url ="https://graph.facebook.com/me"

    params ={

    "fields":fields ,

    "access_token":access_token ,

    }

    response =requests .get (base_url ,params =params )

    user_info =response .json ()

    return user_info

redirect_uri ="https://example.com/auth/facebook/callback"

client_id ="your_facebook_client_id"

client_secret ="your_facebook_client_secret"

scope ="email"

login_url =get_facebook_login_url (redirect_uri ,client_id ,scope )

print ("Login URL:",login_url )

code ="received_code_from_redirect_uri"

print ("Access Token:",access_token )

user_info =get_facebook_user_info (access_token )

print ("User Info:",user_info )