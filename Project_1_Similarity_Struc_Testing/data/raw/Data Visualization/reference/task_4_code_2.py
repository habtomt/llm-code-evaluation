`python

from google.cloud import bigquery



# Create BigQuery client

client = bigquery.Client()



# Perform collaborative filtering and recommendation algorithms on user data

query = """

SELECT 

  recommended_product

FROM 

  user_behavior 

WHERE 

  behavior = 'purchase'

  user_id, 

  recommended_product

"""



recommendations = client.query(query).result()

for row in recommendations:

    print(f"User {row.user_id} may also like {row.recommended_product}")