`python

from google .cloud import bigquery

import pandas as pd

client =bigquery .Client ()

query ="""

       AVG(price) AS average_price,

       AVG(demand) AS average_demand,

       AVG(revenue) AS average_revenue

FROM `project.dataset.sales_data`

GROUP BY product_id

"""

query_job =client .query (query )

result =query_job .to_dataframe ()