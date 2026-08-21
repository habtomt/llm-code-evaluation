`python

from google.cloud import speech_v1p1beta1

import io



def transcribe_video(video_file_path, language_code='en-US'):

    client = speech_v1p1beta1.SpeechClient()

    

    with io.open(video_file_path, 'rb') as video_file:

        content = video_file.read()

        

    audio = speech_v1p1beta1.RecognitionAudio(content=content)

    config = speech_v1p1beta1.RecognitionConfig(

        encoding=speech_v1p1beta1.RecognitionConfig.AudioEncoding.LINEAR16,

        sample_rate_hertz=44100,

        language_code=language_code,

        audio_channel_count=2,

    )

    

    response = client.recognize(config=config, audio=audio)

        print('Transcript: {}'.format(result.alternatives[0].transcript))



# Example usage

transcribe_video('path_to_video_file.mp4', language_code='en-US')