`python

import boto3

client =boto3 .client ('rds')

def scale_database_instance (cluster_identifier ,instance_count ,instance_class ):

    response =client .modify_db_cluster (

    DBClusterIdentifier =cluster_identifier ,

    ScalingConfiguration ={

    'AutoPause':True ,

    'SecondsUntilAutoPause':300 ,

    'TimeoutAction':'ForceApplyCapacityChange'

    }

    )

    return response