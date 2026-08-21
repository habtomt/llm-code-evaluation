`python

from google.cloud import videointelligence



def compress_video(input_file, output_file, bitrate, resolution):

    client = videointelligence.VideoIntelligenceServiceClient()

        "bitrate": bitrate,

        "resolution": resolution

    }



    input_uri = f'gs://bucket_name/{input_file}'

    output_uri = f'gs://bucket_name/{output_file}'



    video_context = types.VideoContext(

        video_config={

            "codec": "h264",

            "config": {

                "bitrate": bitrate,

                "resolution": resolution

            }

        }

    )



    operation = client.annotate_video(

        input_uri, output_uri, video_context=video_context

    )

    result = operation.result()

    

    return result