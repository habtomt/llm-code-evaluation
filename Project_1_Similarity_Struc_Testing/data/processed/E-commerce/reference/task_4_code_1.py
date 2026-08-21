import pandas as pd

from sklearn .model_selection import train_test_split

from sklearn .metrics .pairwise import cosine_similarity

from sklearn .feature_extraction .text import TfidfVectorizer

data =pd .read_csv ('shopify_dataset.csv')

train_data ,test_data =train_test_split (data ,test_size =0.2 ,random_state =42 )

tfidf =TfidfVectorizer (stop_words ='english')

tfidf_matrix =tfidf .fit_transform (train_data ['description'].values .astype ('U'))

cosine_sim =cosine_similarity (tfidf_matrix ,tfidf_matrix )

def get_recommendations (user_id ,num_recommendations =5 ):

    user_products =data [data ['user_id']==user_id ]

    recommended_products =[]

    for product in user_products ['product_id']:

        sim_scores =sorted (sim_scores ,key =lambda x :x [1 ],reverse =True )

        sim_scores =sim_scores [1 :num_recommendations +1 ]

        product_indices =[i [0 ]for i in sim_scores ]

        recommended_products .extend (list (data ['product_id'].iloc [product_indices ]))

    return list (set (recommended_products ))[:num_recommendations ]

user_id =12345

recommendations =get_recommendations (user_id )

print (recommendations )