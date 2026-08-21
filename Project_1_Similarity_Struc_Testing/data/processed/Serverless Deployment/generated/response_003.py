from flask import Flask ,request ,jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app =Flask (__name__ )

basedir =os .path .abspath (os .path .dirname (__file__ ))
app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os .path .join (basedir ,'webhooks.db')
app .config ['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db =SQLAlchemy (app )

class WebhookData (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    payload =db .Column (db .String ,nullable =False )

with app .app_context ():
    db .create_all ()

def handle_webhook (data ):
    try :

        relevant_data =data .get ('relevant_field','default_value')

        new_entry =WebhookData (payload =str (relevant_data ))
        db .session .add (new_entry )
        db .session .commit ()

        return {'message':'Data received and stored'},200

    except Exception as e :
        db .session .rollback ()
        return {'error':'An error occurred','message':str (e )},500

@app .route ('/webhook',methods =['POST'])
def webhook ():

    data =request .json

    if not data :
        return jsonify ({'error':'No data received'}),400

    return handle_webhook (data )

if __name__ =='__main__':
    app .run (port =5000 ,debug =True )