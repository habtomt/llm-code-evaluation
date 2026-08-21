import boto3

import sagemaker

sagemaker_session =sagemaker .Session ()

prefix ='model'

sagemaker_session .download_data (path ='./downloaded_model',bucket =bucket ,key_prefix =prefix )