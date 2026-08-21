

from google.cloud import language_v1

from google.cloud.language_v1 import enums



def analyze_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    type_ = enums.Document.Type.PLAIN_TEXT

    document = {"content": text_content, "type": type_}

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment



def main():

    user_input = input("User: ")

    while user_input.lower() != "exit":

        score, magnitude = analyze_sentiment(user_input)

        if score >= 0:

            print("Bot: That's great to hear!")

            print("Bot: I'm sorry to hear that.")

        user_input = input("User: ")



if __name__ == "__main__":

    main()