import pandas as pd
from sklearn .model_selection import train_test_split
from sklearn .feature_extraction .text import TfidfVectorizer
from sklearn .naive_bayes import MultinomialNB
from sklearn .metrics import classification_report ,accuracy_score
from sklearn .preprocessing import StandardScaler
from sklearn .ensemble import RandomForestClassifier
from sklearn .svm import SVC
from sklearn .linear_model import LogisticRegression
from nltk .corpus import stopwords
from nltk .stem import WordNetLemmatizer
from nltk .tokenize import word_tokenize
import nltk
import re
import numpy as np

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

data =pd .read_csv ("reviews.csv")

data ['review_text']=data ['review_text'].apply (preprocess_text )

X =data ['review_text']
y =data ['label']

X_train ,X_test ,y_train ,y_test =train_test_split (X ,y ,test_size =0.3 ,random_state =42 )

vectorizer =TfidfVectorizer (stop_words ='english',max_features =1000 )

X_train_vectorized =vectorizer .fit_transform (X_train )
X_test_vectorized =vectorizer .transform (X_test )

models ={
'Naive Bayes':MultinomialNB (),
'Random Forest':RandomForestClassifier (),
'SVM':SVC (),
'Logistic Regression':LogisticRegression ()
}

for name ,model in models .items ():
    try :
        model .fit (X_train_vectorized ,y_train )
        y_pred =model .predict (X_test_vectorized )
        print (f"Model: {name}")
        print ("Accuracy:",accuracy_score (y_test ,y_pred ))
        print ("Classification Report:\n",classification_report (y_test ,y_pred ))
        print ()
    except Exception as e :
        print (f"Error with {name}: {e}")