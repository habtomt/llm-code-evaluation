



sagemaker = boto3.client('sagemaker')

# Define the model and deploy it on edge devices

model_data = 's3://your-bucket/model.tar.gz'

device_type = 'jetson-tx2'

accelerator_type = 'NVIDIA_TENSORRT'



response = sagemaker.create_edge_packaging_job(

    RoleArn='arn:aws:iam::123456789012:role/service-role/role-name',

    OutputConfig={

        'S3OutputLocation': 's3://your-bucket/output',

        'KmsKeyId': 'your-kms-key'

    },

    ModelName='your-model',

    ModelVersion='1.0',

    EdgePackagingJobName='your-edge-packaging-job',

    CompilationJobName='your-compilation-job',

    ModelArtifact=model_data,

    DeviceType=device_type,

    CompilationTarget={

        'Device': 'jetson-tx2',

        'Optimization': {

            'Ideal': True,

            'Otfu': True

        },

        'Accelerator': accelerator_type

    }

)



print(response)