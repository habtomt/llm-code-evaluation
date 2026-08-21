from google.cloud import bigquery

import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt



# Set up BigQuery client

client = bigquery.Client()



# Run a query to analyze historical sales data

query = """

SELECT 

    DATE_TRUNC(order_date, month) AS month,

    SUM(sales) AS total_sales

FROM

    `your_project.your_dataset.your_table`

GROUP BY 

    month

ORDER BY 

    month

"""



# Run the query and store the results

query_job = client.query(query)

sales_data = query_job.to_dataframe()



# Visualize the sales data

plt.figure(figsize=(12, 6))

sns.lineplot(x='month', y='total_sales', data=sales_data)

plt.title('Monthly Total Sales')

plt.xlabel('Month')

plt.ylabel('Total Sales')

plt.xticks(rotation=45)

plt.show()