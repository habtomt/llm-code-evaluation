`python

import speech_recognition as sr

from gtts import gTTS

import playsound

client =translate .Client ()

r =sr .Recognizer ()

with sr .Microphone ()as source :

    print ("Speak something in source language:")

    audio =r .listen (source )

    user_input =r .recognize_google (audio )

target_language ='fr'

translation =client .translate (user_input ,target_language )

print (translation ['translatedText'])

tts =gTTS (translation ['translatedText'],lang =target_language )

tts .save ('output.mp3')

playsound .playsound ('output.mp3')