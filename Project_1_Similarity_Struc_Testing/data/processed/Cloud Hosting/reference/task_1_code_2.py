import boto3

import time

import os

def check_if_backup_successful ():

    return True

def backup_data ():

    os .system ('backup_tool_command')

def store_data_in_s3 ():

    s3 =boto3 .client ('s3',region_name ='your_region')

    s3 .upload_file ('local_backup_file','s3_bucket_name','s3_key_name')

def monitor_backup_task ():

    while True :

        is_backup_successful =check_if_backup_successful ()

        if is_backup_successful :

            print ("Backup completed successfully")

            break

        else :

            print ("Backup failed. Retrying...")

            time .sleep (60 )

schedule_backup =True

if schedule_backup :

    while True :

        backup_data ()

        monitor_backup_task ()

        time .sleep (86400 )