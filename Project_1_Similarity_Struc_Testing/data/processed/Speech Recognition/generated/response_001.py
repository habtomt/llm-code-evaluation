import pyaudio
import wave
import speech_recognition as sr
import sqlite3
from tkinter import Tk
from tkinter import filedialog
import os

FORMAT =pyaudio .paInt16
CHANNELS =1
RATE =16000
CHUNK =1024
RECORD_SECONDS =5
WAVE_OUTPUT_FILENAME ="output.wav"

audio =pyaudio .PyAudio ()

def record_audio ():
    print ("Start recording...")
    stream =audio .open (format =FORMAT ,channels =CHANNELS ,
    rate =RATE ,input =True ,
    frames_per_buffer =CHUNK )

    frames =[]

    for i in range (0 ,int (RATE /CHUNK *RECORD_SECONDS )):
        data =stream .read (CHUNK )
        frames .append (data )

    print ("Finished recording.")

    stream .stop_stream ()
    stream .close ()
    audio .terminate ()

    waveFile =wave .open (WAVE_OUTPUT_FILENAME ,'wb')
    waveFile .setnchannels (CHANNELS )
    waveFile .setsampwidth (audio .get_sample_size (FORMAT ))
    waveFile .setframerate (RATE )
    waveFile .writeframes (b''.join (frames ))
    waveFile .close ()

def transcribe_audio ():
    recognizer =sr .Recognizer ()
    with sr .AudioFile (WAVE_OUTPUT_FILENAME )as source :
        audio_data =recognizer .record (source )
        try :

            text =recognizer .recognize_google (audio_data )
            return text
        except sr .UnknownValueError :
            print ("Google Speech Recognition could not understand audio")
            return None
        except sr .RequestError as e :
            print ("Could not request results from Google Speech Recognition service; {0}".format (e ))
            return None

def save_transcription (text ):
    conn =sqlite3 .connect ('transcriptions.db')
    c =conn .cursor ()
    c .execute ('''CREATE TABLE IF NOT EXISTS transcriptions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT)''')
    c .execute ("INSERT INTO transcriptions (text) VALUES (?)",(text ,))
    conn .commit ()
    conn .close ()

def search_transcriptions (query ):
    conn =sqlite3 .connect ('transcriptions.db')
    c =conn .cursor ()
    c .execute ("SELECT text FROM transcriptions WHERE text LIKE ?",('%'+query +'%',))
    results =c .fetchall ()
    return results

root =Tk ()
root .withdraw ()

file_path =filedialog .askdirectory ()
if file_path :

    record_audio ()

    text =transcribe_audio ()
    if text :

        save_transcription (text )

        query =input ("Enter search query: ")
        results =search_transcriptions (query )
        for result in results :
            print (result [0 ])

os .remove (WAVE_OUTPUT_FILENAME )

print ("Transcription tool finished.")