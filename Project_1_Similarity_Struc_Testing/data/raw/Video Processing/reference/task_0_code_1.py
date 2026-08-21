`python

from google.cloud import videointelligence



def compress_video(input_file, output_file, bitrate, resolution):

    client = videointelligence.VideoIntelligenceServiceClient()

    input_uri = "gs://your-bucket-name/" + input_file

    output_uri = "gs://your-bucket-name/" + output_file

    

    config = videointelligence.types.VideoConfig(

        resolution = resolution,

        codec = 'h.264'

    )

    

        input_uri=input_uri,

        output_uri=output_uri,

        features=[videointelligence.Feature.VIDEO_COMPRESSION],

        video_config=config

    )

    

    result = operation.result()

    print('Video compression complete')