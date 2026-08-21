from google .cloud import speech
from google .cloud import dialogflow_v2 as dialogflow
from google .cloud import texttospeech
import pyaudio
import wave

GOOGLE_APPLICATION_CREDENTIALS ="path_to_your_service_account_key.json"

CHUNK =1024
FORMAT =pyaudio .paInt16
CHANNELS =2
RATE =44100
RECORD_SECONDS =5
WAVE_OUTPUT_FILENAME ="output.wav"

def speech_to_text (audio_file_path ):

    client =speech .SpeechClient ()

    with open (audio_file_path ,"rb")as audio_file :
        content =audio_file .read ()

    audio =speech .RecognitionAudio (content =content )

    config =speech .RecognitionConfig (
    encoding =speech .RecognitionConfig .AudioEncoding .LINEAR16 ,
    language_code ="en-US",
    )

    response =client .recognize (config =config ,audio =audio )

    for result in response .results :
        return result .alternatives [0 ].transcript

def get_dialogflow_response (project_id ,session_id ,text_input ,language_code ='en'):

    session_client =dialogflow .SessionsClient ()

    session =session_client .session_path (project_id ,session_id )

    text_input =dialogflow .TextInput (text =text_input ,language_code =language_code )

    query_input =dialogflow .QueryInput (text =text_input )

    response =session_client .detect_intent (session =session ,query_input =query_input )

    return response .query_result .fulfillment_text

def text_to_speech (text ,output_audio_path ):

    client =texttospeech .TextToSpeechClient ()

    synthesis_input =texttospeech .SynthesisInput (text =text )

    voice =texttospeech .VoiceSelectionParams (
    language_code ="en-US",ssml_gender =texttospeech .SsmlVoiceGender .FEMALE
    )

    audio_config =texttospeech .AudioConfig (
    audio_encoding =texttospeech .AudioEncoding .MP3
    )

    response =client .synthesize_speech (input =synthesis_input ,voice =voice ,audio_config =audio_config )

    with open (output_audio_path ,"wb")as out_file :
        out_file .write (response .audio_content )

    print (f'Audio content written to file {output_audio_path}')

def record_audio ():

    p =pyaudio .PyAudio ()

    stream =p .open (format =FORMAT ,channels =CHANNELS ,rate =RATE ,input =True ,frames_per_buffer =CHUNK )

    frames =[]

    print ("Recording...")
    for i in range (0 ,int (RATE /CHUNK *RECORD_SECONDS )):
        data =stream .read (CHUNK )
        frames .append (data )
    print ("Finished recording")

    stream .stop_stream ()
    stream .close ()

    p .terminate ()

    waveFile =wave .open (WAVE_OUTPUT_FILENAME ,'wb')
    waveFile .setnchannels (CHANNELS )
    waveFile .setsampwidth (p .get_sample_size (FORMAT ))
    waveFile .setframerate (RATE )
    waveFile .writeframes (b''.join (frames ))
    waveFile .close ()

def main ():

    record_audio ()

    customer_query =speech_to_text (WAVE_OUTPUT_FILENAME )

    project_id ="your-dialogflow-project-id"
    session_id ="unique-session-id"
    response_text =get_dialogflow_response (project_id ,session_id ,customer_query )

    text_to_speech (response_text ,"response.mp3")

if __name__ =="__main__":
    main ()