import os
import subprocess

def convert_video (input_file ,output_file ,codec ='libx264',resolution =None ,bitrate =None ):

    cmd =['ffmpeg','-i',input_file ,'-c:v',codec ]

    if resolution :
        cmd .extend (['-s',resolution ])

    if bitrate :
        cmd .extend (['-b:v',bitrate ])

    cmd .append (output_file )

    print (f"Running command: {' '.join(cmd)}")
    try :
        subprocess .run (cmd ,check =True )
    except subprocess .CalledProcessError as e :
        print (f"Error: FFmpeg command failed with return code {e.returncode}")
        raise

def main ():
    input_file ='input_video.mp4'
    output_file ='output_video.mp4'

    convert_video (input_file ,output_file ,codec ='libx264',resolution ='1920x1080',bitrate ='500k')

if __name__ =='__main__':
    main ()