`python

from google .cloud import videointelligence

def apply_watermark (input_uri ,output_uri ,watermark_text ,transparency ):

    client =videointelligence .VideoIntelligenceServiceClient ()

    features =[videointelligence .Feature .WATERMARK_DETECTION ]

    mode =videointelligence .WatermarkDetectionConfig .Mode .TRANSPARENT if transparency else videointelligence .WatermarkDetectionConfig .Mode .OPAQUE

    context =videointelligence .VideoContext (watermark_detection_config =detection_config )

    operation =client .annotate_video (input_uri =input_uri ,output_uri =output_uri ,features =features ,video_context =context )

    result =operation .result ()

    print ('Watermark applied successfully')

input_video_uri ='gs://your-bucket/input_video.mp4'

output_video_uri ='gs://your-bucket/output_video.mp4'

watermark_text ='Your Company Name'

transparency =True