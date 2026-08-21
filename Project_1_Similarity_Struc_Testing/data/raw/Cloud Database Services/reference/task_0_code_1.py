`python

import psycopg2

import boto3



on_premise_conn = psycopg2.connect(

    host='on_premise_host',

    database='on_premise_db',

    user='on_premise_user',

    password='on_premise_password'

)

on_premise_cursor = on_premise_conn.cursor()



# Connect to the AWS RDS PostgreSQL instance

aws_rds_conn = psycopg2.connect(

    host='aws_rds_host',

    database='aws_rds_db',

    user='aws_rds_user',

    password='aws_rds_password'

)

aws_rds_cursor = aws_rds_conn.cursor()



# Get on-premise schema

on_premise_cursor.execute("SELECT table_name, column_name, data_type FROM information_schema.columns")

table_columns = on_premise_cursor.fetchall()



# Create tables in AWS RDS

for table, column, data_type in table_columns:

    query = f"CREATE TABLE {table} ({column} {data_type})"

    aws_rds_cursor.execute(query)



# Copy data from on-premise to AWS RDS

on_premise_cursor.execute("SELECT * FROM some_table")

rows = on_premise_cursor.fetchall()

for row in rows:

    query = f"INSERT INTO some_table VALUES {row}"

    aws_rds_cursor.execute(query)



# Check data integrity

aws_count = aws_rds_cursor.fetchone()[0]

on_premise_cursor.execute("SELECT COUNT(*) FROM some_table")

on_premise_count = on_premise_cursor.fetchone()[0]



if on_premise_count == aws_count:

    print("Data migration successful")

else:

    print("Data migration failed")



# Close the connections

on_premise_cursor.close()

on_premise_conn.close()

aws_rds_cursor.close()

aws_rds_conn.close()