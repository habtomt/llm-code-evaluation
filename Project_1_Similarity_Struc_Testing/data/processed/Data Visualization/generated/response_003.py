import pandas as pd
from textblob import TextBlob
import matplotlib .pyplot as plt
from wordcloud import WordCloud

data ={
'date':['2023-09-01','2023-09-02','2023-09-03'],
'text':[
'I love the new product! It\'s amazing.',
'The product is okay, nothing special.',
'I had a terrible experience with the product.'
]
}

def main ():

    df =pd .DataFrame (data )
    df ['date']=pd .to_datetime (df ['date'])

    def analyze_sentiment (text ):

        blob =TextBlob (text )

        return blob .sentiment .polarity

    df ['sentiment']=df ['text'].apply (analyze_sentiment )

    def classify_sentiment (polarity ):

        if polarity >0.1 :
            return 'Positive'
        elif polarity <-0.1 :
            return 'Negative'
        else :
            return 'Neutral'

    df ['sentiment_category']=df ['sentiment'].apply (classify_sentiment )

    try :

        trend =df .groupby ([df ['date'],'sentiment_category']).size ().unstack ().fillna (0 )

        trend .plot (kind ='line',stacked =False ,figsize =(10 ,6 ))
        plt .title ('Sentiment Trend Over Time')
        plt .xlabel ('Date')
        plt .ylabel ('Number of Posts')
        plt .show ()

        def plot_wordcloud (category ):

            text =' '.join (df [df ['sentiment_category']==category ]['text'])

            wordcloud =WordCloud (width =800 ,height =400 ,max_words =100 ,background_color ='white').generate (text )

            plt .figure (figsize =(10 ,6 ))
            plt .imshow (wordcloud ,interpolation ='bilinear')
            plt .axis ('off')
            plt .title (f'Most Common Words in {category} Comments')
            plt .show ()

        plot_wordcloud ('Positive')
        plot_wordcloud ('Negative')
        plot_wordcloud ('Neutral')
    except Exception as e :
        print (f"An error occurred: {e}")

if __name__ =="__main__":
    main ()