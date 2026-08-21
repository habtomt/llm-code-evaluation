`python

import boto3

source_db_info = {

    "host": "on-premise-host",

    "username": "on-premise-username",

    "password": "on-premise-password",

    "database": "on-premise-database"

}



target_db_info = {

    "host": "rds-host",

    "username": "rds-username",

    "password": "rds-password",

}



# Connect to the source and target databases

# Perform schema transfer from source to target

# Migrate data from source to target

# Perform integrity checks to ensure data consistency

# Handle minimal downtime during migration process