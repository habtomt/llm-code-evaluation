import boto3
import sagemaker
from sagemaker import get_execution_role
from sagemaker .predictor import RealTimePredictor
import tensorflow as tf

model_path ='s3://your-bucket/path_to_model/model.tar.gz'

converter =tf .lite .TFLiteConverter .from_saved_model (model_path )
tflite_model =converter .convert ()

with open ('converted_model.tflite','wb')as f :
    f .write (tflite_model )

session =boto3 .Session (profile_name ='your-profile-name')
client =session .client ('mobile')

response =client .create_project (
name ='YourMobileAppProject',
region ='us-east-1',
)

response =client .deploy_to_stage (
projectName ='YourMobileAppProject',
stageName ='prod',
)

interpreter =tf .lite .Interpreter (model_path ="converted_model.tflite")
interpreter .allocate_tensors ()