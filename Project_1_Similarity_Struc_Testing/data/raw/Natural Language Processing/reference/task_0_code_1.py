

from google.cloud import language_v1



client = language_v1.LanguageServiceClient()

response = client.analyze_sentiment(document=document, encoding_type='UTF32')



print('Sentiment Score: {}'.format(response.document_sentiment.score))

print('Sentiment Magnitude: {}'.format(response.document_sentiment.magnitude))