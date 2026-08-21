import subprocess

def reduce_video_size (input_file ,output_file ,target_bitrate =None ,resolution =None ,codec ='libx264'):

    command =['ffmpeg','-i',input_file ,'-c:v',codec ]

    if target_bitrate :
        command .extend (['-b:v',target_bitrate ])

    if resolution :
        command .extend (['-vf',f'scale={resolution}'])

    command .append (output_file )

    try :
        subprocess .run (command ,check =True )
        print (f"Video file compressed and saved as {output_file}")
    except subprocess .CalledProcessError as e :
        print (f"An error occurred while processing the video: {e}")

input_video_path ="YOUR_INPUT_VIDEO_PATH.mp4"
output_video_path ="compressed_video.mp4"
reduce_video_size (input_video_path ,output_video_path ,target_bitrate ='500k',resolution ='1280x720',codec ='libx265')