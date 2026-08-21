`python

from google .cloud import bigquery

from google .cloud import language_v1

import pandas as pd

import matplotlib .pyplot as plt

def analyze_sentiment (text_content ):

    client =language_v1 .LanguageServiceClient ()

    document =language_v1 .Document (content =text_content ,type_ =language_v1 .Document .Type .PLAIN_TEXT )

    response =client .analyze_sentiment (request ={'document':document })

    return response .document_sentiment .score

def main ():

    project_id ='your-project-id'

    client =bigquery .Client (project =project_id )

    query ="""

    SELECT post_date, post_content

    FROM `your-dataset.your-table`

    """

    df =client .query (query ).result ().to_dataframe ()

    sentiment_scores =[]

    for post in df ['post_content']:

        sentiment_scores .append (analyze_sentiment (post ))

    df ['sentiment_score']=sentiment_scores

    df ['post_date']=pd .to_datetime (df ['post_date'])

    plt .plot (df ['post_date'],df ['sentiment_score'])

    plt .xlabel ('Date')

    plt .ylabel ('Sentiment Score')

    plt .title ('Sentiment Analysis over Time')

    plt .show ()

if __name__ =='__main__':