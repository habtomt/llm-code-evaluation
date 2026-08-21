`python

from google .cloud import videointelligence

def analyze_video (input_uri ):

    client =videointelligence .VideoIntelligenceServiceClient ()

    features =[videointelligence .enums .Feature .CELEBRITY_RECOGNITION ,

    videointelligence .enums .Feature .EXPLICIT_CONTENT_DETECTION ,

    videointelligence .enums .Feature .LABEL_DETECTION ]

    operation =client .annotate_video (input_uri =input_uri ,features =features )

    return result

def check_for_inappropriate_content (result ):

    explicit_percentage =result .annotation_results .explicit_annotation .frames [0 ].pornography_likelihood

    if explicit_percentage >0.5 :

        return "Inappropriate content detected"

    else :

        return "No inappropriate content detected"

video_uri ="gs://your-bucket-name/your-video.mp4"

moderation_result =check_for_inappropriate_content (analysis_result )

print (moderation_result )