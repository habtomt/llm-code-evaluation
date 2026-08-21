
from google.cloud import vision

from google.cloud.vision_v1 import types



def enhance_image(image_path):

    client = vision.ImageAnnotatorClient()



    with open(image_path, 'rb') as image_file:

        content = image_file.read()



    image = types.Image(content=content)

    response = client.image_properties(image=image)

    properties = response.image_properties_annotation



    modified_image = image.enhance(brightness=1.2, contrast=1.5, sharpness=2.0)



    # Save the modified image