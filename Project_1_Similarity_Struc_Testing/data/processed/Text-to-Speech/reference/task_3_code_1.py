`python

from google.cloud import texttospeech

def text_to_speech(text, output_file):

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(

        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL

    )

    audio_config = texttospeech.AudioConfig(

        audio_encoding=texttospeech.AudioEncoding.MP3

    )

    response = client.synthesize_speech(

    with open(output_file, "wb") as out:

        out.write(response.audio_content)

directions = "In 500 feet, turn right onto Main Street."

output_file = "directions.mp3"

text_to_speech(directions, output_file)