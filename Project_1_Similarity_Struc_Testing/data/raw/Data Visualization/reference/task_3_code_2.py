`python

from google.cloud import bigquery



client = bigquery.Client()



query = """

SELECT

  TIMESTAMP_TRUNC(created_at, DAY) AS date,

  AVG(CASE WHEN sentiment_score > 0.5 THEN 1 ELSE 0 END) AS positive,

  AVG(CASE WHEN sentiment_score < 0.5 THEN 1 ELSE 0 END) AS negative,

  AVG(CASE WHEN sentiment_score = 0.5 THEN 1 ELSE 0 END) AS neutral

FROM

  `project.dataset.social_media_sentiment_table`

GROUP BY

  date

"""



df = client.query(query).to_dataframe()



# Visualize sentiment trends over time with your preferred plotting library