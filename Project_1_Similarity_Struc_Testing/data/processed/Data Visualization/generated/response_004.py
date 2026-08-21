import pandas as pd
from surprise import Dataset ,Reader
from surprise .model_selection import train_test_split
from surprise import SVD ,accuracy
from surprise import KNNBasic ,KNNWithMeans ,KNNWithZScore
from surprise import NormalPredictor ,BaselineOnly
from surprise import CoClustering
from surprise import SlopeOne
from collections import defaultdict

def load_data ():

    data ={
    'userId':[1 ,2 ,1 ,2 ,3 ],
    'itemId':[101 ,101 ,102 ,103 ,102 ],
    'rating':[5 ,3 ,4 ,2 ,5 ],
    }
    df =pd .DataFrame (data )
    return df

def prepare_data (df ):

    reader =Reader (rating_scale =(1 ,5 ))

    surprise_data =Dataset .load_from_df (df [['userId','itemId','rating']],reader )

    trainset ,testset =train_test_split (surprise_data ,test_size =0.25 )

    return trainset ,testset

def train_model (trainset ):

    model =SVD ()

    model .fit (trainset )

    return model

def evaluate_model (model ,testset ):

    predictions =model .test (testset )

    accuracy .rmse (predictions )

def make_prediction (model ,userId ,itemId ):

    prediction =model .predict (userId ,itemId )
    return prediction .est

def get_top_n_recommendations (model ,userId ,n ):

    items =[iid for iid in range (101 ,104 )]

    predictions =[]
    for iid in items :
        prediction =model .predict (userId ,iid )
        predictions .append ((iid ,prediction .est ))

    predictions .sort (key =lambda x :x [1 ],reverse =True )

    return predictions [:n ]

def main ():
    try :

        df =load_data ()

        trainset ,testset =prepare_data (df )

        model =train_model (trainset )

        evaluate_model (model ,testset )

        prediction =make_prediction (model ,1 ,103 )
        print (f"Predicted rating for user 1 and item 103: {prediction}")

        top_n_recommendations =get_top_n_recommendations (model ,1 ,3 )
        print (f"Top 3 recommendations for user 1: {top_n_recommendations}")

    except Exception as e :
        print (f"An error occurred: {e}")

if __name__ =="__main__":
    main ()