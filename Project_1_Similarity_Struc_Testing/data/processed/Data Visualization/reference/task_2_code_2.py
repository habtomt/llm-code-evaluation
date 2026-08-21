`python

from google .cloud import bigquery

import pandas as pd

client =bigquery .Client ()

query ="""

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

query_job =client .query (query )

results =query_job .result ().to_dataframe ()

plt .figure (figsize =(10 ,6 ))

plt .plot (results ['hour'],results ['pageviews'])

plt .title ('Website Traffic Analysis')

plt .xlabel ('Time')

plt .ylabel ('Pageviews')

plt .show ()