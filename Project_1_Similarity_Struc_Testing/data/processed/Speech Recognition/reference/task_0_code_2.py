`python

from google .cloud import speech

from google .cloud .speech import enums

from google .cloud .speech import types

def speech_to_text (audio_file_path ):

    client =speech .SpeechClient ()

    with open (audio_file_path ,'rb')as audio_file :

        content =audio_file .read ()

    audio =types .RecognitionAudio (content =content )

    config =types .RecognitionConfig (

    encoding =enums .RecognitionConfig .AudioEncoding .LINEAR16 ,

    sample_rate_hertz =16000 ,

    language_code ='en-US',

    model ='command_and_search'

    )

    for result in response .results :

        print ('Transcript: {}'.format (result .alternatives [0 ].transcript ))

if __name__ =='__main__':

    audio_file_path ='path_to_audio_file'