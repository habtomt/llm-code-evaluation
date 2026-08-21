`python

import requests

def authenticate_with_facebook (access_token ):

    user_info_response =requests .get (

    f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"

    )

    user_info =user_info_response .json ()

access_token ="insert_access_token_here"

authenticate_with_facebook (access_token )