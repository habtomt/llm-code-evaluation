`python

from google .cloud import bigquery

client =bigquery .Client ()

query ="""

SELECT

  recommended_product

FROM

  user_behavior

WHERE

  behavior = 'purchase'

  user_id,

  recommended_product

"""

recommendations =client .query (query ).result ()

for row in recommendations :

    print (f"User {row.user_id} may also like {row.recommended_product}")