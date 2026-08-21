`python

from google.cloud import bigquery

import pandas as pd



# Initialize a BigQuery client

client = bigquery.Client()

# Define the query

query = """

SELECT 

    DATETIME_TRUNC(timestamp, HOUR) as hour,

    COUNT(*) as pageviews

FROM 

    `project_id.dataset_id.table_name`

GROUP BY 

    hour

ORDER BY 

    hour

"""



# Make a request to execute the query

query_job = client.query(query)



# Convert the results to a pandas DataFrame

results = query_job.result().to_dataframe()



# Plot the data

plt.figure(figsize=(10, 6))

plt.plot(results['hour'], results['pageviews'])

plt.title('Website Traffic Analysis')

plt.xlabel('Time')

plt.ylabel('Pageviews')

plt.show()