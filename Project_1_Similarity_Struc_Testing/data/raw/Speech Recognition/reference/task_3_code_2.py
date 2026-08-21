`python

from google.cloud import speech_v1

from google.cloud.speech_v1 import enums



def transcribe_audio(audio_file_path):

    client = speech_v1.SpeechClient()

    

    with io.open(audio_file_path, "rb") as audio_file:

        content = audio_file.read()



    audio = {"content": content}

    config = {

    }



    response = client.recognize(config=config, audio=audio)

    

    for result in response.results:

        print("Transcript: {}".format(result.alternatives[0].transcript))