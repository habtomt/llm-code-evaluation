`python

import requests

import json

import matplotlib .pyplot as plt

def get_facebook_data (api_key ,page_id ):

    url =f'https://graph.facebook.com/v12.0/{page_id}/insights?metric=page_fans,page_engaged_users,page_impressions,page_video_views&access_token={api_key}'

    response =requests .get (url )

    data =response .json ()

    return data

def generate_dashboard (data ):

    metrics =data ['data']

    page_fans =metrics [0 ]['values'][0 ]['value']

    page_engaged_users =metrics [1 ]['values'][0 ]['value']

    page_impressions =metrics [2 ]['values'][0 ]['value']

    page_video_views =metrics [3 ]['values'][0 ]['value']

    labels =['Page Fans','Engaged Users','Impressions','Video Views']

    plt .bar (labels ,values )

    plt .title ('Facebook Analytics')

    plt .ylabel ('Count')

    plt .show ()

api_key ='your_api_key'

page_id ='your_page_id'

facebook_data =get_facebook_data (api_key ,page_id )

generate_dashboard (facebook_data )