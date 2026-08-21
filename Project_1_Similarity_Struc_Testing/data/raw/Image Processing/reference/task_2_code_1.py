

from google.cloud import vision

import io



client = vision.ImageAnnotatorClient()



# Load image

with io.open('image.jpg', 'rb') as image_file:

    content = image_file.read()



image = vision.Image(content=content)



# Perform object detection

response = client.object_localization(image=image)



for obj in objects:

    print(f'{obj.name} (confidence: {obj.score})')