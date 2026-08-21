

from google.cloud import language_v1

from google.cloud.language_v1 import enums



def detect_entities(text_content):

    client = language_v1.LanguageServiceClient()

    language = "en"

    document = {"content": text_content, "type": type_, "language": language}

    response = client.analyze_entities(document=document)

    for entity in response.entities:

        print(u"Entity name: {}".format(entity.name))

        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))

        print(u"Salience score: {}".format(entity.salience))