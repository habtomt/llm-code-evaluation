import boto3
import mysql .connector
from mysql .connector import errorcode
import os

DB_INSTANCE_IDENTIFIER ="mydbinstance"
DB_NAME ="mydatabase"
MASTER_USERNAME ="admin"
REGION ="us-west-2"
KMS_KEY_ARN ="arn:aws:kms:us-west-2:123456789012:key/abcd-1234-abcd-1234-abcd1234abcd"
SECURITY_GROUP_ID ="sg-0123456789abcdef0"
MASTER_PASSWORD ="YOUR_MASTER_PASSWORD"

def create_rds_instance ():
    try :
        rds =boto3 .client ('rds',region_name =REGION )
        response =rds .create_db_instance (
        DBInstanceIdentifier =DB_INSTANCE_IDENTIFIER ,
        DBInstanceClass ='db.m5.large',
        Engine ='mysql',
        MasterUsername =MASTER_USERNAME ,
        MasterUserPassword =MASTER_PASSWORD ,
        StorageEncrypted =True ,
        KmsKeyId =KMS_KEY_ARN ,
        AllocatedStorage =20 ,
        BackupRetentionPeriod =7 ,
        VpcSecurityGroupIds =[SECURITY_GROUP_ID ],
        DBName =DB_NAME
        )
        print ("RDS instance created successfully.")
        return response ['DBInstance']['DBInstanceIdentifier']
    except Exception as e :
        print (f"Error creating RDS instance: {e}")

def wait_for_db_instance (db_instance_identifier ):
    try :
        rds =boto3 .client ('rds',region_name =REGION )
        rds .get_waiter ('db_instance_available').wait (DBInstanceIdentifier =db_instance_identifier )
        print ("DB instance is available.")
    except Exception as e :
        print (f"Error waiting for DB instance: {e}")

def enable_ssl_connections (db_endpoint ):
    try :

        cnx =mysql .connector .connect (
        user =MASTER_USERNAME ,
        password =MASTER_PASSWORD ,
        host =db_endpoint ,
        ssl_ca ='/path/to/ssl/ca-cert.pem',
        ssl_cert ='/path/to/ssl/client-cert.pem',
        ssl_key ='/path/to/ssl/client-key.pem'
        )
        cursor =cnx .cursor ()
        cursor .execute ("REVOKE USAGE ON *.* FROM 'mysql_insecure_user'@'%'")
        cursor .execute ("GRANT USAGE ON *.* TO 'mysql_insecure_user'@'%' REQUIRE SSL")
        cursor .execute ("FLUSH PRIVILEGES")
        cnx .commit ()
        cursor .close ()
        cnx .close ()
        print ("SSL connections enabled successfully.")
    except mysql .connector .Error as err :
        print (f"Error enabling SSL connections: {err}")

def setup_role_based_access_control (db_endpoint ):
    try :

        cnx =mysql .connector .connect (
        user =MASTER_USERNAME ,
        password =MASTER_PASSWORD ,
        host =db_endpoint
        )
        cursor =cnx .cursor ()

        cursor .execute ("CREATE ROLE 'readonly'")
        cursor .execute ("CREATE ROLE 'readwrite'")

        cursor .execute (f"GRANT SELECT ON {DB_NAME}.* TO 'readonly'")
        cursor .execute (f"GRANT SELECT, INSERT, UPDATE, DELETE ON {DB_NAME}.* TO 'readwrite'")

        cursor .execute ("GRANT 'readonly' TO 'user_read'@'%'")
        cursor .execute ("GRANT 'readwrite' TO 'user_write'@'%'")
        cursor .execute ("FLUSH PRIVILEGES")
        cnx .commit ()
        cursor .close ()
        cnx .close ()
        print ("Role-based access control setup successfully.")
    except mysql .connector .Error as err :
        print (f"Error setting up role-based access control: {err}")

def enable_audit_logging (db_instance_identifier ):
    try :
        rds =boto3 .client ('rds',region_name =REGION )
        response =rds .modify_db_instance (
        DBInstanceIdentifier =db_instance_identifier ,
        CloudwatchLogsExportConfiguration ={
        'EnableLogTypes':['audit','slowquery']
        },
        ApplyImmediately =True
        )
        print ("Audit logging enabled successfully.")
    except Exception as e :
        print (f"Error enabling audit logging: {e}")

def main ():
    db_instance_identifier =create_rds_instance ()
    wait_for_db_instance (db_instance_identifier )
    rds =boto3 .client ('rds',region_name =REGION )
    response =rds .describe_db_instances (DBInstanceIdentifier =db_instance_identifier )
    db_endpoint =response ['DBInstances'][0 ]['Endpoint']['Address']
    enable_ssl_connections (db_endpoint )
    setup_role_based_access_control (db_endpoint )
    enable_audit_logging (db_instance_identifier )
    print ("Security configurations have been applied to your RDS instance.")

if __name__ =="__main__":
    main ()