`python

import boto3

import pandas as pd

import numpy as np

from sklearn .cluster import KMeans

from sklearn .preprocessing import StandardScaler

redshift =boto3 .client ('redshift')

query ="SELECT * FROM customer_data"

response =redshift .execute_statement (ClusterIdentifier ='mycluster',Database ='mydb',Sql =query )

data =pd .DataFrame (response ['records'])

scaler =StandardScaler ()

kmeans =KMeans (n_clusters =3 )

kmeans .fit (scaled_data )

data ['Cluster']=kmeans .labels_