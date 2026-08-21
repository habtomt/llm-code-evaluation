`python

from google.cloud import bigquery



client = bigquery.Client()



# Query the operational data for analysis

query = """

SELECT 

    department,

    AVG(processing_time) AS avg_processing_time,

    MAX(processing_time) AS max_processing_time,

    MIN(processing_time) AS min_processing_time

FROM 

    operational_data

GROUP BY 

"""



# Execute the query

query_job = client.query(query)



# Display the results

for row in query_job:

    print(row)