

import sagemaker

from sagemaker import get_execution_role

from sagemaker.model import Model

from sagemaker.predictor import RealTimePredictor



role = get_execution_role()

sess = sagemaker.Session()

bucket = 'your-bucket'

prefix = 'your-prefix'



model = Model(model_data='s3://{}/{}/model.tar.gz'.format(bucket, prefix),

              image='your-edge-optimized-image',

              role=role)



predictor = model.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')