`python

import requests

import schedule

import time

def post_to_facebook ():

    access_token ='ACCESS_TOKEN'

    post_data ={

    'message':'Your post message here',

    }

    response =requests .post (f'https://graph.facebook.com/me/feed?access_token={access_token}',data =post_data )

    print ("Posted to Facebook")

schedule .every ().day .at ("09:00").do (post_to_facebook )

while True :

    schedule .run_pending ()

    time .sleep (1 )