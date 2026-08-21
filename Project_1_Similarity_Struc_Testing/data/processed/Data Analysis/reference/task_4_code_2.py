`python

from google .cloud import bigquery

client =bigquery .Client ()

query ="""

SELECT

    department,

    AVG(processing_time) AS avg_processing_time,

    MAX(processing_time) AS max_processing_time,

    MIN(processing_time) AS min_processing_time

FROM

    operational_data

GROUP BY

"""

query_job =client .query (query )

for row in query_job :

    print (row )