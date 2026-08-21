`python

from google.cloud.speech import enums

from google.cloud.speech import types



def transcribe_audio(audio_file):

    client = speech.SpeechClient()



    with open(audio_file, 'rb') as audio_file:

        content = audio_file.read()



    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(

        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,

        sample_rate_hertz=16000,

        language_code='en-US'



    response = client.recognize(config=config, audio=audio)



    for result in response.results:

        print('Transcript: {}'.format(result.alternatives[0].transcript))



# Call the function with the audio file path

transcribe_audio('path_to_audio_file')