import os
import sys
import json
from flask import Flask ,request ,send_file ,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug .utils import secure_filename
import subprocess
from pydub import AudioSegment
from pydub .utils import make_chunks
from pydub import AudioSegment
from pydub .playback import play
from pydub .utils import which
import time
import threading
import datetime
from flask import send_from_directory
from flask import after_this_request
from werkzeug .utils import secure_filename

app =Flask (__name__ )
CORS (app )
app .config ['SQLALCHEMY_DATABASE_URI']='sqlite:///videos.db'
db =SQLAlchemy (app )

class Video (db .Model ):
    id =db .Column (db .Integer ,primary_key =True )
    title =db .Column (db .String (100 ),nullable =False )
    description =db .Column (db .String (200 ),nullable =False )
    upload_time =db .Column (db .DateTime ,nullable =False ,default =datetime .datetime .utcnow )

UPLOAD_FOLDER ='uploads'
app .config ['UPLOAD_FOLDER']=UPLOAD_FOLDER
if not os .path .exists (UPLOAD_FOLDER ):
    os .makedirs (UPLOAD_FOLDER )

with app .app_context ():
    db .create_all ()

def convert_video_to_hls (video_path ):
    output_dir =f"streams/{os.path.basename(video_path)}"
    if not os .path .exists (output_dir ):
        os .makedirs (output_dir )
    command =f"ffmpeg -i {video_path} -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {output_dir}/index.m3u8"
    subprocess .run (command ,shell =True )
    return output_dir

def upload_video (file ):
    video_path =os .path .join (app .config ['UPLOAD_FOLDER'],secure_filename (file .filename ))
    file .save (video_path )
    output_dir =convert_video_to_hls (video_path )
    video =Video (title ='Untitled',description ='No description',upload_time =datetime .datetime .utcnow ())
    db .session .add (video )
    db .session .commit ()
    return output_dir

@app .route ('/upload',methods =['POST'])
def upload ():
    file =request .files ['video']
    output_dir =upload_video (file )
    return jsonify ({'output_dir':output_dir })

@app .route ('/stream/<path:path>')
def stream (path ):
    @after_this_request
    def remove_file (response ):
        try :
            os .remove (f"streams/{path}")
        except Exception as error :
            print (error )
        return response
    return send_from_directory ('streams',path ,as_attachment =True )

if __name__ =='__main__':
    app .run (debug =True )