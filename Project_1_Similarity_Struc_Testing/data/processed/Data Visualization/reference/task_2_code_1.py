`python

import pandas as pd

import seaborn as sns

import matplotlib .pyplot as plt

client =bigquery .Client ()

query ="""

SELECT

  date,

  EXTRACT(HOUR FROM time) as hour,

  COUNT(DISTINCT user_id) as unique_visitors,

  AVG(page_views) as avg_page_views

FROM

  `project_name.dataset_name.table_name`

GROUP BY

  date, hour

ORDER BY

  date, hour

"""

query_job =client .query (query )

website_traffic_data =query_job .to_dataframe ()

peak_traffic_times =website_traffic_data .groupby ('hour')['unique_visitors'].sum ()

plt .figure (figsize =(10 ,6 ))

sns .lineplot (x =peak_traffic_times .index ,y =peak_traffic_times .values )

plt .title ('Peak Traffic Times')

plt .xlabel ('Hour of the Day')

plt .ylabel ('Number of Unique Visitors')

plt .show ()

user_demographics ="""

SELECT

  gender,

  COUNT(DISTINCT user_id) as user_count

  `project_name.dataset_name.table_name`

GROUP BY

  gender

"""

user_demographics_query_job =client .query (user_demographics )

user_demographics_data =user_demographics_query_job .to_dataframe ()

plt .figure (figsize =(8 ,5 ))

sns .barplot (x ='gender',y ='user_count',data =user_demographics_data )

plt .title ('User Demographics')

plt .xlabel ('Gender')

plt .ylabel ('Number of Users')

plt .show ()

engagement_metrics ="""

SELECT

  AVG(time_spent) as avg_time_spent,

  AVG(page_views) as avg_page_views

FROM

  `project_name.dataset_name.table_name`

"""

engagement_metrics_query_job =client .query (engagement_metrics )

engagement_metrics_data =engagement_metrics_query_job .to_dataframe ()

print (engagement_metrics_data )