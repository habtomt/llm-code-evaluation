

from google.cloud import language_v1

from google.cloud.language_v1 import enums



def analyze_text_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT

    document = {"content": text_content, "type": type_, "language": language}

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment.score

    return sentiment



def respond_conversationally(user_input):

    sentiment = analyze_text_sentiment(user_input)

    if sentiment > 0:

        return "That's great to hear!"

    elif sentiment < 0:

        return "I'm sorry to hear that."

        return "Thanks for sharing."



user_input = input("Enter your message: ")

response = respond_conversationally(user_input)

print(response)