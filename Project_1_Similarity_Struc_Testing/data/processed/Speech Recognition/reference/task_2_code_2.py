`python

from google .cloud import speech_v1

from google .cloud .speech_v1 import enums

import os

os .environ ["GOOGLE_APPLICATION_CREDENTIALS"]="path_to_service_account_key.json"

    client =speech_v1 .SpeechClient ()

    config ={

    "language_code":language_code ,

    "encoding":encoding ,

    }

    audio ={"content":input_audio }

    response =client .recognize (config =config ,audio =audio )

    for result in response .results :

        return result .alternatives [0 ].transcript

input_audio =b"audio_content"

language_code ="en-US"

transcript =detect_intent_audio (input_audio ,language_code )

print (transcript )