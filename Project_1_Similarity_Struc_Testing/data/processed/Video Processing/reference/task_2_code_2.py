`python

from google .cloud import videointelligence_v1p3beta1 as videointelligence

def stabilize_video (input_uri ,output_uri ):

    client =videointelligence .VideoIntelligenceServiceClient ()

    features =[videointelligence .Feature .SHOT_CHANGE_DETECTION ,videointelligence .Feature .STABILIZATION ]

    context ={"video_config":{"feature":videointelligence .Feature .STABILIZATION ,"stabilization_config":{"stabilization_mode":"SMOOTH"}}}

    operation =client .annotate_video (input_uri =input_uri ,features =features ,output_uri =output_uri ,video_context =context )

    result =operation .result ()

    print (f"Stabilized video saved to: {output_uri}")

input_uri ="gs://your-bucket-name/your-input-video.mp4"

stabilize_video (input_uri ,output_uri )