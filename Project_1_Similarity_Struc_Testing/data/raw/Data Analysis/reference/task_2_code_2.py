`python

from google.cloud import bigquery



# Initialize a BigQuery client

client = bigquery.Client()



# Perform SQL query to evaluate marketing campaign effectiveness

query = """

SELECT

    marketing_campaign,

    COUNT(DISTINCT user_id) as conversion_rate,

    (revenue - cost) / cost as ROI,

    SUM(page_views) / COUNT(DISTINCT user_id) as customer_engagement

FROM

    marketing_campaign_data

WHERE

    date BETWEEN 'start_date' AND 'end_date'

GROUP BY

    marketing_campaign

"""



# Execute the query

query_job = client.query(query)

# Fetch the results

results = query_job.result()

# Display the results

for row in results:

    print(row)