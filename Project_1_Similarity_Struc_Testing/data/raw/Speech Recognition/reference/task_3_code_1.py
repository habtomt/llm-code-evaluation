`python

import io



client = speech.SpeechClient()

config = {

    "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,

    "language_code": "en-US",

}

operation = client.long_running_recognize(config=config, audio=audio)

response = operation.result(timeout=90)



for result in response.results:

    print("Transcript: {}".format(result.alternatives[0].transcript))