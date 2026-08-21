from google .cloud import vision
import io

client =vision .ImageAnnotatorClient ()

uri ="gs://your-bucket-name/your-image.jpg"

image =vision .Image ()
image .source .image_uri =uri

response =client .object_localization (
image =image
)
objects =response .localized_object_annotations

if objects :
    for object_ in objects :
        print (f'{object_.name} (confidence: {object_.score})')