`python

from google .cloud import bigquery

client =bigquery .Client ()

query ="""

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

query_job =client .query (query )

results =query_job .result ()

for row in results :

    print (row )