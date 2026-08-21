`python

from google .cloud import speech_v1p1beta1

from google .cloud .speech_v1p1beta1 import enums

import io

client =speech_v1p1beta1 .SpeechClient ()

language_code ="en-US"

config ={

"sample_rate_hertz":16000 ,

"language_code":language_code ,

"alternative_language_codes":["es-ES"],

}

audio ={"uri":"gs://cloud-samples-data/speech/brooklyn_bridge.raw"}

for result in response .results :

    print ("Transcript: {}".format (result .alternatives [0 ].transcript ))