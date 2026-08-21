import requests
from flask import Flask ,render_template
import json

def fetch_facebook_data (api_key ):

    url =f'https://graph.facebook.com/me?access_token={api_key}'
    response =requests .get (url )
    return response .json ()

def fetch_twitter_data (api_key ,api_secret_key ):

    url ="https://api.twitter.com/2/tweets"
    headers ={"Authorization":f"Bearer {api_key}"}
    params ={"ids":"123456789"}
    response =requests .get (url ,headers =headers ,params =params )
    return response .json ()

def aggregate_data (facebook_data ,twitter_data ):

    aggregated_data ={
    'total_posts':facebook_data .get ('posts_count',0 )+twitter_data .get ('tweets_count',0 ),
    'follower_growth':facebook_data .get ('new_followers',0 )+twitter_data .get ('new_followers',0 ),
    'engagement_rate':(facebook_data .get ('engagement',0 )+twitter_data .get ('engagement',0 ))/2 ,
    }
    return aggregated_data

app =Flask (__name__ )

@app .route ('/')
def dashboard ():
    try :

        facebook_data =fetch_facebook_data ('your_facebook_api_key')
        twitter_data =fetch_twitter_data ('your_twitter_api_key','your_twitter_api_secret_key')

        data =aggregate_data (facebook_data ,twitter_data )

        return render_template ('dashboard.html',data =json .dumps (data ))
    except Exception as e :

        return f"An error occurred: {str(e)}"

@app .route ('/static/css/style.css')
def style ():
    return render_template ('style.css')

@app .route ('/static/js/script.js')
def script ():
    return render_template ('script.js')

if __name__ =='__main__':

    app .run (debug =True )