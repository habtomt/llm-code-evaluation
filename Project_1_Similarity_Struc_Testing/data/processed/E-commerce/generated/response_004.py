import pandas as pd
from sklearn .model_selection import train_test_split
from scipy .sparse .linalg import svds
import numpy as np

def load_data (file_path ):
    try :
        ratings_data =pd .read_csv (file_path )
        return ratings_data
    except Exception as e :
        print (f"Error loading data: {e}")

def prepare_data (ratings_data ):
    try :

        train_data ,test_data =train_test_split (ratings_data ,test_size =0.2 ,random_state =42 )
        return train_data ,test_data
    except Exception as e :
        print (f"Error preparing data: {e}")

def build_recommendation_system (train_data ):
    try :

        user_product_matrix =train_data .pivot (index ='user_id',columns ='product_id',values ='rating').fillna (0 )
        matrix =user_product_matrix .to_numpy ()

        user_ratings_mean =np .mean (matrix ,axis =1 )
        matrix_demeaned =matrix -user_ratings_mean .reshape (-1 ,1 )

        U ,sigma ,Vt =svds (matrix_demeaned ,k =50 )

        sigma =np .diag (sigma )

        predicted_ratings =np .dot (np .dot (U ,sigma ),Vt )+user_ratings_mean .reshape (-1 ,1 )
        predicted_ratings_df =pd .DataFrame (predicted_ratings ,columns =user_product_matrix .columns )
        return predicted_ratings_df
    except Exception as e :
        print (f"Error building recommendation system: {e}")

def recommend_products (predicted_ratings_df ,user_id ,num_recommendations =5 ):
    try :
        user_index =user_id -1
        sorted_user_predictions =predicted_ratings_df .iloc [user_index ].sort_values (ascending =False )

        user_data =train_data [train_data .user_id ==user_id ]
        user_rated_products =user_data .product_id .values

        recommendations =sorted_user_predictions [~sorted_user_predictions .index .isin (user_rated_products )].head (num_recommendations )

        print ("Recommendations for User ID:",user_id )
        print (recommendations )
    except Exception as e :
        print (f"Error making recommendations: {e}")

def main ():
    file_path ='user_product_ratings.csv'
    ratings_data =load_data (file_path )
    train_data ,test_data =prepare_data (ratings_data )
    predicted_ratings_df =build_recommendation_system (train_data )
    recommend_products (predicted_ratings_df ,user_id =1 ,num_recommendations =5 )

if __name__ =="__main__":
    main ()