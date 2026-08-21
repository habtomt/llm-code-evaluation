

# Use Shopify's open-source services to build a system for product recommendation using collaborative filtering and machine learning techniques



# Import necessary libraries

import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics.pairwise import pairwise_distances

from scipy.sparse import csr_matrix

from sklearn.neighbors import NearestNeighbors



# Load the user interaction data

user_interactions = pd.read_csv('user_interactions.csv')



# Pivot the data to create a user-item matrix

interaction_matrix = user_interactions.pivot_table(index='user_id', columns='product_id', values='interaction_type', fill_value=0)



# Convert the pivot table to a sparse matrix

interaction_matrix_sparse = csr_matrix(interaction_matrix.values)



model = NearestNeighbors(metric='cosine', algorithm='brute')

model.fit(interaction_matrix_sparse)



# Generate personalized recommendations for a specific user

user_id = 123

user_row_index = interaction_matrix.index.get_loc(user_id)

distances, indices = model.kneighbors(interaction_matrix.iloc[user_row_index, :].values.reshape(1, -1), n_neighbors=5)



# Get product recommendations for the user

for index in indices.flatten():

    product_id = interaction_matrix.index[index]

    recommended_products.append(product_id)



print(f"Recommended products for user {user_id}: {recommended_products}")