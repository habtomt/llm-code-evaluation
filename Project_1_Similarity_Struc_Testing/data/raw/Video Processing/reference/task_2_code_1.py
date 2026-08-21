`python

from google.cloud import videointelligence_v1p3beta1 as videointelligence



def video_stabilization(input_uri, output_uri):

    client = videointelligence.VideoIntelligenceServiceClient()

    input_mode = videointelligence.Feature.VideoSegment

    config = videointelligence.VideoConfig(

        feature=input_mode, 

        file_uri=input_uri, 

        video_stabilization_config={"stabilize": True}

    )

    context = videointelligence.VideoContext(

        segments=None, 

        label_detection_mode=None, 

        face_detection_mode=None, 

        video_classification_mode=None, 

        shot_change_detection_mode=None, 

        explicit_content_detection_mode=None

    )

        features=[config], 

        video_context=context, 

        output_uri=output_uri

    )

    result = operation.result()

    return result