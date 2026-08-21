import sagemaker

from sagemaker import get_execution_role

from sagemaker .estimator import Estimator

from sagemaker .predictor import RealTimePredictor

from sagemaker .model_monitor import DataCaptureConfig

from sagemaker .model_monitor import CronExpressionGenerator

from sagemaker .model_monitor .dataset_format import DatasetFormat

from sagemaker .predictor import Predictor

from sagemaker import image_uris

role =get_execution_role ()

estimator =Estimator (image_uri =image_uris .retrieve (framework ="tensorflow",region ="us-east-1",version ="2.3.1"),

role =role ,

instance_count =1 ,

instance_type ='ml.m4.xlarge',

entry_point ='train_deploy.py')

predictor =estimator .deploy (initial_instance_count =1 ,instance_type ='ml.m4.xlarge')

data_capture_config =DataCaptureConfig (

enable_capture =True ,

sampling_percentage =100 ,

destination_s3_uri ='s3://sagemaker-data-capture'

)

predictor .update_data_capture_config (data_capture_config =data_capture_config )

model_quality_monitor =DefaultModelMonitor (

role =role ,

instance_count =1 ,

instance_type ='ml.m4.xlarge',

max_runtime_in_seconds =1800

)

model_quality_monitor .create_monitoring_schedule (cron_expression =CronExpressionGenerator .hourly (),

endpoint_input =predictor .endpoint )