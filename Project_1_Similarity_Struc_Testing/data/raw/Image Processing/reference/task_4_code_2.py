import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import enums

def image_segmentation(image_path):
    client = vision_v1.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.types.Image(content=content)
    response = client.image_properties(image=image)
    properties = response.image_properties_annotation

    try:
        request = vision_v1.types.AnnotateImageRequest(image=image, features=[segmented_image])
        response = client.annotate_image(request)

        for segment in response.image_properties_annotation:
            print("Segment bounds:")
            for bound in segment.bounding_poly.normalized_vertices:
                print(f" - ({bound.x}, {bound.y})")
    except NameError:
        pass

image_path = "path/to/your/image.jpg"
image_segmentation(image_path)