`python

import pandas as pd

from fbprophet import Prophet

client =bigquery .Client ()

query ="""

SELECT

  date,

  SUM(sales) as total_sales

FROM

  `project.dataset.sales_table`

GROUP BY

  date

ORDER BY

  date

"""

df =client .query (query ).to_dataframe ()

df =df .rename (columns ={'date':'ds','total_sales':'y'})

model =Prophet ()

model .fit (df )

future =model .make_future_dataframe (periods =365 )

forecast =model .predict (future )

fig =model .plot (forecast )