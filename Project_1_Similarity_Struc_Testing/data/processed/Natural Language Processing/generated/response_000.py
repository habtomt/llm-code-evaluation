from textblob import TextBlob

def analyze_sentiment (text ):
    try :

        blob =TextBlob (text )

        sentiment =blob .sentiment

        polarity =sentiment .polarity
        subjectivity =sentiment .subjectivity

        if polarity >0 :
            sentiment_label ="Positive"
        elif polarity <0 :
            sentiment_label ="Negative"
        else :
            sentiment_label ="Neutral"

        return sentiment_label ,polarity ,subjectivity

    except Exception as e :

        print (f"An error occurred: {e}")
        return None

text ="I love this product! It works wonderfully."
result =analyze_sentiment (text )

if result :
    sentiment_label ,polarity ,subjectivity =result
    print (f"Sentiment: {sentiment_label}")
    print (f"Polarity: {polarity}")
    print (f"Subjectivity: {subjectivity}")
else :
    print ("Failed to analyze sentiment.")