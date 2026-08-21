`python

from google .cloud import videointelligence

def transcode_video (input_uri ,output_uri ,output_format ):

    client =videointelligence .VideoIntelligenceServiceClient ()

    input_video =videointelligence .types .VideoContext (uri =input_uri )

    output_video =videointelligence .types .VideoConfig (

    uri =output_uri ,

    spec ={'codec':output_format }

    )

    result =operation .result ()

    print ('Video transcoding complete: {}'.format (result ))

input_uri ='gs://input-video-bucket/input_video.mp4'

output_uri ='gs://output-video-bucket/output_video.webm'

output_format ='webm'

transcode_video (input_uri ,output_uri ,output_format )