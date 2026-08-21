`python

from google.cloud import videointelligence



def check_video_for_inappropriate_content(uri):

    client = videointelligence.VideoIntelligenceServiceClient()

    

    config.include_adult = True

    config.include_violence = True



    video_context = videointelligence.types.VideoContext()

    video_context.safe_search_detection_config = config



    operation = client.annotate_video(input_uri=uri, features=[videointelligence.Feature.SAFE_SEARCH_DETECTION], video_context=video_context)

    result = operation.result()



    explicit_frame_count = 0

    violent_frame_count = 0

    for frame in result.annotation_results[0].safe_search_annotations:

        if frame.time_offset is not None:

            print(f'Time offset: {frame.time_offset.seconds}.{(frame.time_offset.nanos / 1e6) :.0f}')

            print(f'Explicit content likelihood: {frame.explicit_content_likelihood.name}')

            print(f'Violent content likelihood: {frame.violent_content_likelihood.name}')

            if frame.explicit_content_likelihood > videointelligence.Likelihood.POSSIBLE:

                explicit_frame_count += 1

                violent_frame_count += 1



    print(f'Total frames with explicit content: {explicit_frame_count}')

    print(f'Total frames with violent content: {violent_frame_count}')