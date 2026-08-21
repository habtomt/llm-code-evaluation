`python

import vimeo_ott

client =vimeo_ott .Client (api_key ='your_api_key_here')

video =client .create_video (title ='My Video',description ='This is my video')

video .upload (file_path ='path_to_video_file.mp4')

video .category ='Entertainment'

video .save ()

video_url =video .get_adaptive_stream ()

print (video_url )