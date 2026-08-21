import boto3
import json
from datetime import datetime

def create_rds_snapshot (db_instance_identifier ,region_name ='us-west-2'):

    rds_client =boto3 .client ('rds',region_name =region_name )

    snapshot_identifier =f"{db_instance_identifier}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    response =rds_client .create_db_snapshot (
    DBInstanceIdentifier =db_instance_identifier ,
    DBSnapshotIdentifier =snapshot_identifier
    )

    print ("RDS snapshot created:",response )
    return snapshot_identifier

def store_snapshot_to_s3 (s3_bucket ,snapshot_identifier ,region_name ='us-west-2'):

    rds_client =boto3 .client ('rds',region_name =region_name )

    export_task =rds_client .start_export_task (
    ExportTaskIdentifier =snapshot_identifier ,
    SourceArn =f'arn:aws:rds:{region_name}:123456789012:snapshot:{snapshot_identifier}',
    S3BucketName =s3_bucket ,
    IamRoleArn ='arn:aws:iam::123456789012:role/MyRDSExportRole',
    KmsKeyId ='your-kms-key-id'
    )
    print ("Started export task:",export_task )

def lambda_handler (event ,context ):

    db_instance_identifier ='your_db_instance_identifier'
    s3_bucket ='your_s3_bucket_name'

    snapshot_identifier =create_rds_snapshot (db_instance_identifier )

    store_snapshot_to_s3 (s3_bucket ,snapshot_identifier )

    return {
    'statusCode':200 ,
    'body':json .dumps ('Backup process started')
    }

if __name__ =='__main__':

    snapshot_identifier =create_rds_snapshot ('your_db_instance_identifier')

    store_snapshot_to_s3 ('your_s3_bucket_name',snapshot_identifier )

    lambda_handler ({},{})