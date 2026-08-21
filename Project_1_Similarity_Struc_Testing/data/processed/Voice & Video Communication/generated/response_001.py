import pyaudio
import socket
import numpy as np
import wave
import webrtcvad
import keyboard
import threading

CHUNK =1024
FORMAT =pyaudio .paInt16
CHANNELS =1
RATE =16000
SERVER_ADDRESS =('127.0.0.1',12345 )
PTT_KEY ='space'

audio =pyaudio .PyAudio ()

vad =webrtcvad .Vad ()
vad .set_mode (3 )

def capture_audio_and_send ():

    stream =audio .open (format =FORMAT ,channels =CHANNELS ,
    rate =RATE ,input =True ,frames_per_buffer =CHUNK )

    sock =socket .socket (socket .AF_INET ,socket .SOCK_DGRAM )

    print ("Press push-to-talk button to start speaking...")

    try :
        while True :

            data =stream .read (CHUNK )

            if vad .is_speech (data ,RATE )and is_ptt_key_pressed ():
                sock .sendto (data ,SERVER_ADDRESS )

    except KeyboardInterrupt :
        print ("Stopping audio capture.")

    finally :
        stream .stop_stream ()
        stream .close ()
        sock .close ()

def receive_and_play_audio ():
    stream =audio .open (format =FORMAT ,channels =CHANNELS ,
    rate =RATE ,output =True ,frames_per_buffer =CHUNK )

    sock =socket .socket (socket .AF_INET ,socket .SOCK_DGRAM )
    sock .bind (SERVER_ADDRESS )

    print ("Listening for audio...")

    try :
        while True :
            data ,addr =sock .recvfrom (CHUNK )
            stream .write (data )

    except KeyboardInterrupt :
        print ("Audio playback stopped.")

    finally :
        stream .stop_stream ()
        stream .close ()
        sock .close ()

def is_ptt_key_pressed ():

    if keyboard .is_pressed (PTT_KEY ):
        return True
    return False

def listen_for_key_press ():
    while True :
        if is_ptt_key_pressed ():
            print ("Push-to-talk button pressed.")
        else :
            print ("Push-to-talk button released.")

send_thread =threading .Thread (target =capture_audio_and_send )
receive_thread =threading .Thread (target =receive_and_play_audio )
key_press_thread =threading .Thread (target =listen_for_key_press )

send_thread .start ()
receive_thread .start ()
key_press_thread .start ()

send_thread .join ()
receive_thread .join ()
key_press_thread .join ()

audio .terminate ()