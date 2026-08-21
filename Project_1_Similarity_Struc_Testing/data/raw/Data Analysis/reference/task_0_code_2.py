from google.cloud import bigquery

import pandas as pd

import matplotlib.pyplot as plt



# Create a client to connect to BigQuery

client = bigquery.Client()



# Define the query to retrieve historical sales data

query = """

SELECT 

    EXTRACT(YEAR FROM date) AS sales_year,

    EXTRACT(MONTH FROM date) AS sales_month,

    SUM(revenue) AS total_revenue

FROM 

    `project.dataset.sales_data`

GROUP BY 

    sales_year, sales_month

ORDER BY 

    sales_year, sales_month

"""



# Make a request to BigQuery and store the results in a pandas dataframe

df = client.query(query).result().to_dataframe()



# Analyze historical sales data using statistical techniques and visualization tools

# E.g., calculating moving averages, identifying trends, plotting time series, etc.



# Example: Plotting the monthly total revenue over time

plt.figure(figsize=(10, 6))

plt.plot(range(len(df)), df['total_revenue'], marker='o')

plt.xlabel('Month')

plt.ylabel('Total Revenue')

plt.title('Monthly Total Revenue Over Time')

plt.xticks(range(len(df)), [f"{y}-{m:02d}" for y, m in zip(df['sales_year'], df['sales_month'])], rotation=45)

plt.show()