`python

import pandas as pd

import psycopg2

from sklearn .cluster import KMeans

from sklearn .decomposition import PCA

import matplotlib .pyplot as plt

import seaborn as sns

conn =psycopg2 .connect (

dbname ='your_dbname',

user ='your_username',

password ='your_password',

host ='your_redshift_cluster_endpoint',

port ='your_redshift_cluster_port'

)

query ="SELECT customer_id, purchase_behavior, demographics, relevant_metrics FROM customer_table"

customer_data =pd .read_sql (query ,conn )

scaler =StandardScaler ()

scaled_data =scaler .fit_transform (customer_data [['purchase_behavior','demographics','relevant_metrics']])

pca =PCA (n_components =2 )

pca_data =pca .fit_transform (scaled_data )

kmeans =KMeans (n_clusters =3 ,random_state =42 )

customer_data ['cluster']=kmeans .fit_predict (pca_data )

plt .figure (figsize =(10 ,6 ))

sns .scatterplot (x =pca_data [:,0 ],y =pca_data [:,1 ],hue =customer_data ['cluster'],palette ='viridis')

plt .xlabel ('PCA Component 1')

plt .ylabel ('PCA Component 2')

plt .show ()