

from google.cloud import language_v1

from google.cloud.language_v1 import Document, LanguageServiceClient



def summarize_text(text):

    document = Document(content=text, type_=Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(request={'document': document})

    return summary