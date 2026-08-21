import pandas as pd
from sklearn .feature_extraction .text import TfidfVectorizer
from sklearn .model_selection import train_test_split
from sklearn .linear_model import LogisticRegression
from sklearn .metrics import classification_report
import nltk
from nltk .corpus import stopwords
from nltk .tokenize import word_tokenize
from nltk .stem import WordNetLemmatizer
import re

nltk .download ('punkt')
nltk .download ('wordnet')
nltk .download ('stopwords')

def preprocess_text (text ):

    text =text .lower ()

    text =re .sub (r'[^a-zA-Z\s]','',text )

    tokens =word_tokenize (text )

    stop_words =set (stopwords .words ('english'))
    tokens =[token for token in tokens if token not in stop_words ]

    lemmatizer =WordNetLemmatizer ()
    tokens =[lemmatizer .lemmatize (token )for token in tokens ]

    text =' '.join (tokens )

    return text

try :
    data =pd .read_csv ('dataset.csv')
except FileNotFoundError :
    print ("The dataset file was not found. Please ensure it is in the correct location.")
    exit ()

data ['text']=data ['text'].apply (preprocess_text )

X_train ,X_test ,y_train ,y_test =train_test_split (data ['text'],data ['label'],test_size =0.2 ,random_state =42 )

vectorizer =TfidfVectorizer (max_features =10000 )
X_train_tfidf =vectorizer .fit_transform (X_train )
X_test_tfidf =vectorizer .transform (X_test )

model =LogisticRegression ()
model .fit (X_train_tfidf ,y_train )

predictions =model .predict (X_test_tfidf )
print (classification_report (y_test ,predictions ))

def is_inappropriate_post (post ):

    post =preprocess_text (post )

    post_tfidf =vectorizer .transform ([post ])

    prediction =model .predict (post_tfidf )

    return prediction [0 ]==1

new_post ="This is a sample inappropriate comment!"
if is_inappropriate_post (new_post ):
    print ("Inappropriate post detected!")
else :
    print ("Post is appropriate.")