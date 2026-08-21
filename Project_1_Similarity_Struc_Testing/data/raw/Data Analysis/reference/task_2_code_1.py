`python

from google.cloud import bigquery



project_id = 'your-project-id'



# Create a Client object

client = bigquery.Client(project=project_id)



# Write the SQL query to evaluate the marketing campaign effectiveness

query = """

SELECT

  campaign_id,

  SUM(conversions) AS total_conversions,

  SUM(revenue) AS total_revenue,

  COUNT(*) AS total_customers,

  SUM(revenue) / SUM(spend) AS ROI,

  (SUM(conversions) / COUNT(*)) * 100 AS conversion_rate

FROM

  `your_dataset.your_table`

WHERE

  date BETWEEN 'start_date' AND 'end_date'

GROUP BY

  campaign_id

"""



query_job = client.query(query)



# Get the results

results = query_job.result()



# Display the results

for row in results:

    print("Campaign ID: {}, Total Conversions: {}, Total Revenue: {}, Total Customers: {}, ROI: {}, Conversion Rate: {}"

          .format(row.campaign_id, row.total_conversions, row.total_revenue, row.total_customers, row.ROI, row.conversion_rate))