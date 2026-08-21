import nltk
from nltk .tokenize import word_tokenize
from textblob import TextBlob

try :
    nltk .data .find ('tokenizers/punkt')
except LookupError :
    nltk .download ('punkt')
try :
    nltk .data .find ('taggers/averaged_perceptron_tagger')
except LookupError :
    nltk .download ('averaged_perceptron_tagger')

banned_words ={'abuse','dumb','stupid','hate'}

def filter_comment (comment ):

    words =word_tokenize (comment .lower ())

    for word in words :
        if word in banned_words :
            return False

    analysis =TextBlob (comment )
    if analysis .sentiment .polarity <-0.5 :
        return False

    return True

comments =[
"I think this article is stupid and dumb.",
"I disagree with the points made here, but respect your opinion.",
"What a wonderful article, very insightful!"
]

filtered_comments =[comment for comment in comments if filter_comment (comment )]

print ("Filtered Comments:")
for comment in filtered_comments :
    print ("-",comment )

from sklearn .feature_extraction .text import TfidfVectorizer
from sklearn .model_selection import train_test_split
from sklearn .naive_bayes import MultinomialNB
from sklearn .metrics import accuracy_score

train_comments =[
("This is a great article!",1 ),
("I hate this article.",-1 ),
("The article is okay, I guess.",0 ),

]

train_comments_text =[comment for comment ,_ in train_comments ]
train_comments_labels =[label for _ ,label in train_comments ]

train_text ,test_text ,train_labels ,test_labels =train_test_split (train_comments_text ,train_comments_labels ,test_size =0.2 ,random_state =42 )

vectorizer =TfidfVectorizer ()

X_train =vectorizer .fit_transform (train_text )
y_train =train_labels
X_test =vectorizer .transform (test_text )

clf =MultinomialNB ()
clf .fit (X_train ,y_train )

y_pred =clf .predict (X_test )

accuracy =accuracy_score (test_labels ,y_pred )
print (f"Model Accuracy: {accuracy:.2f}")

def enhanced_filter_comment (comment ):

    words =word_tokenize (comment .lower ())

    for word in words :
        if word in banned_words :
            return False

    analysis =TextBlob (comment )
    if analysis .sentiment .polarity <-0.5 :
        return False

    comment_vector =vectorizer .transform ([comment ])
    prediction =clf .predict (comment_vector )
    if prediction [0 ]==-1 :
        return False

    return True

enhanced_filtered_comments =[comment for comment in comments if enhanced_filter_comment (comment )]

print ("Enhanced Filtered Comments:")
for comment in enhanced_filtered_comments :
    print ("-",comment )