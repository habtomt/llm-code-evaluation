`python

from google.cloud import videointelligence_v1p3beta1 as videointelligence

def apply_video_watermark(input_uri, output_uri, watermark_image_uri, opacity):

    client = videointelligence.VideoIntelligenceServiceClient()

    features = [videointelligence.Feature.OBJECT_TRACKING]

    config = {

        "object_tracking_config": {

            "track_object_type": "LOGO",

            "min_object_confidence": 0.6

    }

    input_content = {"uri": input_uri}

    output_uri = output_uri

    watermark_path = watermark_image_uri

    job = {

        "input_uri": input_uri,

        "output_uri": output_uri,

        "features": features,

        "mode": mode,

        "config": config,

        "watermark_path": watermark_path,

        "opacity": opacity

    }

    operation = client.annotate_video(request={"job": job})

    result = operation.result()

    print("Watermarking complete.")