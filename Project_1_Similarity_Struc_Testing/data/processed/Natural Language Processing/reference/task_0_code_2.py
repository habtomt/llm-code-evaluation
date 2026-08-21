from google .cloud import language_v1

def analyze_sentiment (text_content ):

    client =language_v1 .LanguageServiceClient ()

    type_ =language_v1 .Document .Type .PLAIN_TEXT

    language ="en"

    document ={"content":text_content ,"type":type_ ,"language":language }

    response =client .analyze_sentiment (request ={'document':document })

    sentiment =response .document_sentiment

    print (f"Sentiment score: {sentiment.score}")

    print (f"Sentiment magnitude: {sentiment.magnitude}")

text ="I love this product, it's amazing!"

analyze_sentiment (text )