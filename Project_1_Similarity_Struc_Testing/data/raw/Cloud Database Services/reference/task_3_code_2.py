`python

import boto3

import datetime



# Set the AWS region

region_name = 'your_region'





# Set the database identifier

db_identifier = 'your_db_identifier'



# Set the S3 bucket name for storing backups

bucket_name = 'your_bucket_name'



# Schedule the backup using AWS Lambda and CloudWatch Events

def schedule_backup(event, context):

    snapshot_id = 'snapshot-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    rds_client.create_db_snapshot(DBSnapshotIdentifier=snapshot_id, DBInstanceIdentifier=db_identifier)

    s3_client = boto3.client('s3', region_name=region_name)

    s3_client.upload_file(snapshot_id, bucket_name, snapshot_id)



# Versioning of backups can be managed using S3 bucket versioning

s3 = boto3.resource('s3')

bucket_versioning = s3.BucketVersioning(bucket_name)

bucket_versioning.enable()



# The backups are stored in a distributed and secure manner in the specified S3 bucket



# Restoration of backups can be done by downloading the snapshot from S3 and restoring the RDS instance from the snapshot

def restore_backup(snapshot_id):

    s3_client = boto3.client('s3', region_name=region_name)

    s3_client.download_file(bucket_name, snapshot_id, snapshot_id)

    rds_client.restore_db_instance_from_db_snapshot(

        DBInstanceIdentifier=db_identifier + '-restored',

        DBSnapshotIdentifier=snapshot_id

    )