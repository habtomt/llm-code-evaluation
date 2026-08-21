`python

from google .cloud import speech_v1p1beta1

from google .cloud .speech_v1p1beta1 import enums

import io

def transcribe_audio (audio_file_path ):

    client =speech_v1p1beta1 .SpeechClient ()

    with io .open (audio_file_path ,"rb")as audio_file :

        content =audio_file .read ()

    audio ={"content":content }

    config ={

    "language_code":"en-US",

    "sample_rate_hertz":44100 ,

    "encoding":enums .RecognitionConfig .AudioEncoding .LINEAR16 ,

    }

    response =client .recognize (config =config ,audio =audio )

        print ("Transcript: {}".format (result .alternatives [0 ].transcript ))

transcribe_audio ("path_to_audio_file.wav")