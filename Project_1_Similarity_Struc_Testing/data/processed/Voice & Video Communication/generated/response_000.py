import socket
import json
import threading
import pyaudio
import wave
from datetime import datetime
from pydub import AudioSegment
import numpy as np
import pydub .exceptions

class SignalingServer :
    def __init__ (self ):
        self .server_socket =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )
        self .server_socket .bind (('localhost',3000 ))
        self .server_socket .listen (5 )
        print ("Signaling server listening on port 3000")

    def handle_client (self ,client_socket ):
        while True :
            try :
                data =client_socket .recv (1024 )
                if not data :
                    break
                data =json .loads (data .decode ('utf-8'))
                if data ['type']=='offer':

                    print ("Broadcasting offer to",data ['target'])
                    for socket in self .sockets :
                        if socket !=client_socket :
                            socket .sendall (json .dumps ({'type':'offer','data':data ['data']}).encode ('utf-8'))
                elif data ['type']=='answer':

                    print ("Sending answer to",data ['target'])
                    for socket in self .sockets :
                        if socket !=client_socket :
                            socket .sendall (json .dumps ({'type':'answer','data':data ['data']}).encode ('utf-8'))
                elif data ['type']=='candidate':

                    print ("Sending candidate to",data ['target'])
                    for socket in self .sockets :
                        if socket !=client_socket :
                            socket .sendall (json .dumps ({'type':'candidate','data':data ['data']}).encode ('utf-8'))
                elif data ['type']=='disconnect':
                    print ("User disconnected")
                    break
            except Exception as e :
                print ("Error handling client:",e )
                break

    def start (self ):
        self .sockets =[]
        while True :
            client_socket ,address =self .server_socket .accept ()
            print ("Connected to",address )
            self .sockets .append (client_socket )
            threading .Thread (target =self .handle_client ,args =(client_socket ,)).start ()

class STUNServer :
    def __init__ (self ):
        self .server_socket =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )
        self .server_socket .bind (('localhost',3478 ))
        self .server_socket .listen (5 )
        print ("STUN server listening on port 3478")

    def handle_client (self ,client_socket ):
        while True :
            try :
                data =client_socket .recv (1024 )
                if not data :
                    break
                print ("Received data:",data .decode ('utf-8'))
                response =b"Success"
                client_socket .sendall (response )
            except Exception as e :
                print ("Error handling client:",e )
                break

    def start (self ):
        while True :
            client_socket ,address =self .server_socket .accept ()
            print ("Connected to",address )
            threading .Thread (target =self .handle_client ,args =(client_socket ,)).start ()

class MediaServer :
    def __init__ (self ):
        self .server_socket =socket .socket (socket .AF_INET ,socket .SOCK_STREAM )
        self .server_socket .bind (('localhost',8080 ))
        self .server_socket .listen (5 )
        print ("Media server listening on port 8080")

    def handle_client (self ,client_socket ):
        while True :
            try :
                data =client_socket .recv (1024 )
                if not data :
                    break
                print ("Received data:",data .decode ('utf-8'))
                response =b"Success"
                client_socket .sendall (response )
            except Exception as e :
                print ("Error handling client:",e )
                break

    def start (self ):
        while True :
            client_socket ,address =self .server_socket .accept ()
            print ("Connected to",address )
            threading .Thread (target =self .handle_client ,args =(client_socket ,)).start ()

class AudioRecorder :
    def __init__ (self ):
        self .audio =pyaudio .PyAudio ()

    def record (self ,filename ):
        stream =self .audio .open (format =pyaudio .paInt16 ,channels =1 ,rate =44100 ,input =True ,frames_per_buffer =1024 )
        frames =[]
        print ("Recording...")
        while True :
            data =stream .read (1024 )
            frames .append (data )
            if len (frames )>=10 :
                break
        stream .stop_stream ()
        stream .close ()
        self .audio .terminate ()
        print ("Recording finished")
        wf =wave .open (filename ,'wb')
        wf .setnchannels (1 )
        wf .setsampwidth (self .audio .get_sample_size (pyaudio .paInt16 ))
        wf .setframerate (44100 )
        wf .writeframes (b''.join (frames ))
        wf .close ()

    def play (self ,filename ):
        stream =self .audio .open (format =pyaudio .paInt16 ,channels =1 ,rate =44100 ,output =True )
        wf =wave .open (filename ,'rb')
        data =wf .readframes (1024 )
        while data !=b'':
            stream .write (data )
            data =wf .readframes (1024 )
        stream .stop_stream ()
        stream .close ()
        self .audio .terminate ()

signaling_server =SignalingServer ()
signaling_thread =threading .Thread (target =signaling_server .start )
signaling_thread .daemon =True
signaling_thread .start ()

stun_server =STUNServer ()
stun_thread =threading .Thread (target =stun_server .start )
stun_thread .daemon =True
stun_thread .start ()

media_server =MediaServer ()
media_thread =threading .Thread (target =media_server .start )
media_thread .daemon =True
media_thread .start ()

recorder =AudioRecorder ()
recorder .record ('test.wav')

recorder .play ('test.wav')