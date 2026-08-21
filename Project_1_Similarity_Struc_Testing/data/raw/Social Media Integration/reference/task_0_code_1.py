`python

import requests



def authenticate_with_facebook(access_token):

    user_info_response = requests.get(

        f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}"

    )

    user_info = user_info_response.json()

    # Use user_info to create or update user profiles in your application

# Implement a system to redirect users to Facebook OAuth page to get the access token

# Handle the redirect and obtain the access token

access_token = "insert_access_token_here"

authenticate_with_facebook(access_token)