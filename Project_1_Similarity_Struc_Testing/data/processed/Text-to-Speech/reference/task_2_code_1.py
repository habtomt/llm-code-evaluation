`python

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

synthesis_input = texttospeech.SynthesisInput(text="Hello, world!")

    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

)

audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

response = client.synthesize_speech(

    input=synthesis_input, voice=voice, audio_config=audio_config

)

    out.write(response.audio_content)