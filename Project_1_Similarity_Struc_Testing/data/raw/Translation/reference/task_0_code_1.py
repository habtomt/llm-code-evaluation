`python

import speech_recognition as sr

from gtts import gTTS

import playsound



# Initialize Google Cloud Translation API client

client = translate.Client()



# Record user input in source language

r = sr.Recognizer()

with sr.Microphone() as source:

    print("Speak something in source language:")

    audio = r.listen(source)

    user_input = r.recognize_google(audio)



target_language = 'fr'  # replace with target language code

translation = client.translate(user_input, target_language)



# Output the translated text to user

print(translation['translatedText'])



# Convert translated text to speech and play the audio

tts = gTTS(translation['translatedText'], lang=target_language)

tts.save('output.mp3')

playsound.playsound('output.mp3')