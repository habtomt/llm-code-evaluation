`python

from google.cloud import speech

from google.cloud.speech import enums



def transcribe_video(video_file):

    client = speech.SpeechClient()



    with open(video_file, 'rb') as audio_file:

        content = audio_file.read()



    audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(

        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,

        language_code='en-US'

    )



    response = client.recognize(config=config, audio=audio)



    for result in response.results:

        print('Transcript: {}'.format(result.alternatives[0].transcript))



transcribe_video(video_file)