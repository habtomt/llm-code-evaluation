`python

s3 =boto3 .resource ('s3')

s3 .create_bucket (Bucket ='my-distributed-file-system',CreateBucketConfiguration ={

'LocationConstraint':'us-west-1'})

data =open ('file.txt','rb')

s3 .Bucket ('my-distributed-file-system').put_object (Key ='file.txt',Body =data )

s3 .Bucket ('my-distributed-file-system').download_file ('file.txt','downloaded_file.txt')