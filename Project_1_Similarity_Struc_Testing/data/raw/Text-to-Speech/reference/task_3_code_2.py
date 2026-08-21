`python

from google.cloud import texttospeech



    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

        language_code=language_code, ssml_gender=ssml_gender, name=voice_name

    )

    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)



    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)



    with open('output.mp3', 'wb') as out:

        out.write(response.audio_content)