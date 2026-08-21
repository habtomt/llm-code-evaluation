import websockets
import asyncio
import aiohttp
import json
import base64
from cryptography .fernet import Fernet
import boto3

transcribe =boto3 .client ('transcribe')
s3 =boto3 .client ('s3')

key =Fernet .generate_key ()
cipher_suite =Fernet (key )

user_credentials ={
"user1":"password1",
"user2":"password2"
}

async def handle_connection (websocket ,path ):

    query_params =await websocket .recv ()
    query_params =json .loads (query_params )
    username =query_params .get ('username')
    password =query_params .get ('password')

    if username in user_credentials and user_credentials [username ]==password :

        await handle_call (websocket ,path ,username )
    else :
        await websocket .close (code =1008 ,reason ="Authentication failed")

async def handle_call (websocket ,path ,username ):

    offer =await websocket .recv ()
    offer =json .loads (offer )

    answer =await handle_offer (offer )
    answer =json .dumps (answer )

    await websocket .send (answer )

async def handle_offer (offer ):

    pc =websockets .legacy .create_connection ('ws://localhost:8765')

    await pc .send (json .dumps (offer ))

    answer =await pc .recv ()
    answer =json .loads (answer )

    pc .close ()

    return answer

def analyze_transcripts ():

    for recording in list_recordings ():
        job_name =start_transcription_job (recording )
        wait_for_job_to_complete (job_name )
        analyze_transcription_results (job_name )

def list_recordings ():

    return ["recording1","recording2"]

def start_transcription_job (recording ):

    transcribe .start_transcription_job (
    TranscriptionJobName ="transcription-job",
    Media ={"MediaFileUri":"s3://bucket/recording.mp4"},
    MediaFormat ="mp4",
    LanguageCode ="en-US",
    MediaSampleRateHertz =44100 ,
    MediaFormat ="mp4",
    MediaChannelCount =2 ,
    OutputBucketName ="bucket"
    )
    return "transcription-job"

def wait_for_job_to_complete (job_name ):

    while True :
        status =transcribe .get_transcription_job (TranscriptionJobName =job_name )
        if status ["TranscriptionJob"]["TranscriptionJobStatus"]=="COMPLETED":
            break
        else :
            time .sleep (5 )

def analyze_transcription_results (job_name ):

    response =transcribe .get_transcription_job (TranscriptionJobName =job_name )
    transcription =response ["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    with open (transcription ,'r')as file :
        data =file .read ()

    print (data )

async def main ():
    async with websockets .serve (handle_connection ,"localhost",8765 ):
        await asyncio .Future ()

asyncio .run (main ())