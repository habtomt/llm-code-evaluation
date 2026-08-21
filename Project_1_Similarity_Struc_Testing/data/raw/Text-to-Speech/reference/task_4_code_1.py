`python

from google.cloud import texttospeech



    client = texttospeech.TextToSpeechClient()



    input_text = texttospeech.SynthesisInput(text=text)



    voice = texttospeech.VoiceSelectionParams(

        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

    )



    audio_config = texttospeech.AudioConfig(

        audio_encoding=texttospeech.AudioEncoding.MP3

    )



    response = client.synthesize_speech(

        input=input_text, voice=voice, audio_config=audio_config

    )



    with open(output_filename, "wb") as out:

        print(f'Audio content written to file "{output_filename}"')



text = "Once upon a time, in a land far, far away..."

output_filename = "output.mp3"

synthesize_text(text, output_filename)