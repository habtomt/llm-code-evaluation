`python

from google.cloud import videointelligence_v1p3beta1 as videointelligence



def video_enhancement(input_uri, output_uri):

    client = videointelligence.VideoIntelligenceServiceClient()



    config = videointelligence.VideoEnhancementConfig(

        color_adjustment=videointelligence.Color(),

        contrast_enhancement=videointelligence.Contrast(),

        brightness_adjustment=videointelligence.Brightness(),

    )



    context = videointelligence.VideoContext(video_enhancement_config=config)



    operation = client.annotate_video(

        input_uri=input_uri,

        output_uri=output_uri,

        features=[videointelligence.Feature.VIDEO_ENHANCEMENT],

        video_context=context

    )



    print('Processing video enhancement...')



    result = operation.result()



    print('Video enhancement complete')

input_uri = 'gs://path_to_input_video/video.mp4'

output_uri = 'gs://path_to_output_video/enhanced_video.mp4'



video_enhancement(input_uri, output_uri)