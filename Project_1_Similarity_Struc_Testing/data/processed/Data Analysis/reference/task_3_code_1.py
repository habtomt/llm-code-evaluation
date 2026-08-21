`python

from google.cloud import bigquery

from google.cloud.bigquery import magics

client = bigquery.Client()

SELECT product_id,

       COUNT(sales) AS total_sales,

       SUM(revenue) AS total_revenue

FROM my_dataset.my_sales_table

GROUP BY product_id

"""

df = client.query(sql_query).to_dataframe()