`python

import schedule

import time

def post_to_facebook_graph_api (access_token ,message ):

    url =f"https://graph.facebook.com/me/feed?message={message}&access_token={access_token}"

    response =requests .post (url )

    return response .json ()

def schedule_post_to_facebook (access_token ,message ,post_time ):

    while True :

        schedule .run_pending ()

        time .sleep (1 )