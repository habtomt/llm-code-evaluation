`python

import boto3

from datetime import datetime



# Set up AWS credentials

aws_access_key = 'your_access_key'

aws_secret_key = 'your_secret_key'

region_name = 'your_region'



# Connect to RDS

client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region_name)



# Schedule and trigger database backup

def create_db_snapshot(db_instance_identifier, snapshot_name):

    response = client.create_db_snapshot(

        DBSnapshotIdentifier=snapshot_name,

        DBInstanceIdentifier=db_instance_identifier

    )

    print(response)

# Versioning of backups

def tag_db_snapshot(snapshot_name, tag_key, tag_value):

    response = client.add_tags_to_resource(

        ResourceName=snapshot_name,

        Tags=[

            {

                'Key': tag_key,

                'Value': tag_value

            },

        ]

    )

    print(response)



# Store in a distributed and secure manner

def copy_db_snapshot(snapshot_name, target_region):

    cross_region_client = boto3.client('rds', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=target_region)

    response = cross_region_client.copy_db_snapshot(

        TargetDBSnapshotIdentifier=f'{snapshot_name}_copy_{datetime.now().strftime("%Y%m%d%H%M%S")}',

        SourceRegion=region_name

    )

    print(response)



# Easy restoration

def restore_db_from_snapshot(snapshot_name, db_instance_identifier):

    response = client.restore_db_instance_from_db_snapshot(

        DBInstanceIdentifier=db_instance_identifier,

        DBSnapshotIdentifier=snapshot_name,

        PubliclyAccessible=True

    )

    print(response)



# Example usage

db_instance_identifier = 'your_db_identifier'

snapshot_name = f'{db_instance_identifier}_backup_{datetime.now().strftime("%Y%m%d%H%M%S")}'

create_db_snapshot(db_instance_identifier, snapshot_name)

tag_db_snapshot(snapshot_name, 'version', '1.0')

copy_db_snapshot(snapshot_name, 'target_region')

restore_db_from_snapshot(snapshot_name, f'{db_instance_identifier}_restored')