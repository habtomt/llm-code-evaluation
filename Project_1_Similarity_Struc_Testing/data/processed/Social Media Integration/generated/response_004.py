import sqlite3
import tweepy
import schedule
import time
from datetime import datetime

api_key ='YOUR_API_KEY'
api_secret ='YOUR_API_SECRET'
access_token ='YOUR_ACCESS_TOKEN'
access_token_secret ='YOUR_ACCESS_TOKEN_SECRET'

def get_twitter_client ():
    auth =tweepy .OAuth1UserHandler (api_key ,api_secret ,access_token ,access_token_secret )
    return tweepy .API (auth )

def add_post (content ,schedule_time ):
    conn =sqlite3 .connect ('scheduler.db')
    cursor =conn .cursor ()
    cursor .execute ("INSERT INTO posts (content, schedule_time) VALUES (?, ?)",(content ,schedule_time ))
    conn .commit ()
    conn .close ()

def post_to_twitter (content ):
    client =get_twitter_client ()
    try :
        client .update_status (content )
        print (f"Posted to Twitter: {content}")
    except Exception as e :
        print (f"Error posting to Twitter: {str(e)}")

def job_checker ():
    try :
        conn =sqlite3 .connect ('scheduler.db')
        cursor =conn .cursor ()

        current_time =datetime .now ().strftime ('%Y-%m-%d %H:%M:00')
        cursor .execute ("SELECT id, content FROM posts WHERE schedule_time = ?",(current_time ,))

        posts_to_publish =cursor .fetchall ()
        for post_id ,content in posts_to_publish :

            post_to_twitter (content )

            cursor .execute ("DELETE FROM posts WHERE id = ?",(post_id ,))
            conn .commit ()

        conn .close ()
    except Exception as e :
        print (f"Error checking for scheduled posts: {str(e)}")

def create_database ():
    conn =sqlite3 .connect ('scheduler.db')
    cursor =conn .cursor ()
    cursor .execute ('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            schedule_time TEXT NOT NULL
        )
    ''')
    conn .commit ()
    conn .close ()

create_database ()

schedule .every (1 ).minutes .do (job_checker )

add_post ('Hello World! #myfirstpost','2023-10-15 10:30:00')
add_post ('This is another post! #mysecondpost','2023-10-15 10:40:00')

while True :
    schedule .run_pending ()
    time .sleep (1 )