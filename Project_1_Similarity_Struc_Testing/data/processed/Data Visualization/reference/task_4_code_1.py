`python

from google .cloud import bigquery_storage_v1

import pandas as pd

from surprise import Dataset ,Reader ,SVD

from surprise .model_selection import cross_validate

client =bigquery .Client ()

query ="""

SELECT user_id, product_id, rating

FROM `project.dataset.user_product_ratings`

"""

df =client .query (query ).to_dataframe ()

reader =Reader (rating_scale =(1 ,5 ))

data =Dataset .load_from_df (df [['user_id','product_id','rating']],reader )

model =SVD ()

cross_validate (model ,data ,measures =['RMSE','MAE'],cv =5 ,verbose =True )