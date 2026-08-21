from flask import Flask ,jsonify ,request
import socketio
import geolocation
from datetime import datetime
import logging

logging .basicConfig (level =logging .INFO )
logger =logging .getLogger (__name__ )

app =Flask (__name__ )

sio =socketio .Server ()

app .wsgi_app =socketio .WSGIApp (sio ,app .wsgi_app )

responders ={}

@sio .on ('connect')
def connect (sid ,environ ):
    logger .info (f'Responder connected: {sid}')

@sio .on ('disconnect')
def disconnect (sid ):
    logger .info (f'Responder disconnected: {sid}')

    if sid in responders :
        del responders [sid ]
        sio .emit ('responders-updated',responders )

@sio .on ('location-update')
def location_update (sid ,data ):

    responders [sid ]=data
    logger .info (f'Responder {sid} location updated: {data}')
    sio .emit ('responders-updated',responders )

if __name__ =='__main__':
    sio .run (app ,host ='localhost',port =3000 )

class MobileApp :
    def __init__ (self ):
        self .socket =socketio .Client ()
        self .socket .connect ('http://localhost:3000')

    def send_location_update (self ,latitude ,longitude ):
        self .socket .emit ('location-update',{'latitude':latitude ,'longitude':longitude })

    def close_connection (self ):
        self .socket .disconnect ()

class DispatchSystem :
    def __init__ (self ):
        self .socket =socketio .Client ()
        self .socket .connect ('http://localhost:3000')

    def get_responders (self ):
        @sio .on ('responders-updated')
        def responders_updated (data ):
            return data
        return responders_updated (None )

    def close_connection (self ):
        self .socket .disconnect ()

class Map :
    def __init__ (self ):
        self .socket =socketio .Client ()
        self .socket .connect ('http://localhost:3000')

    def get_responders (self ):
        @sio .on ('responders-updated')
        def responders_updated (data ):
            return data
        return responders_updated (None )

    def display_responders (self ,responders ):

        for responder ,location in responders .items ():
            print (f'Responder {responder} is at {location["latitude"]}, {location["longitude"]}')

    def close_connection (self ):
        self .socket .disconnect ()

if __name__ =='__main__':
    try :
        mobile_app =MobileApp ()
        while True :

            latitude =37.7749
            longitude =-122.4194
            mobile_app .send_location_update (latitude ,longitude )

            import time
            time .sleep (1 )
    except KeyboardInterrupt :
        mobile_app .close_connection ()