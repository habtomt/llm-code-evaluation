`python

from google.cloud import bigquery

client = bigquery.Client()

query = """

    SELECT

        AVG(process_time) AS avg_process_time,

        SUM(case when status = 'delayed' then 1 else 0 end) AS delayed_tasks,

        SUM(case when status = 'incomplete' then 1 else 0 end) AS incomplete_tasks

    FROM

        `your_project_name.dataset_name.table_name`

    GROUP BY

        department

query_job = client.query(query)

results = query_job.result()

for row in results:

    print("Department: {}, Average Process Time: {}, Delayed Tasks: {}, Incomplete Tasks: {}".format(row.department, row.avg_process_time, row.delayed_tasks, row.incomplete_tasks))