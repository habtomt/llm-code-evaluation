`python

bucket_name ='my-iot-data-bucket'

object_key ='iot-device-stream-data.txt'

iot_data ="{'device_id': '12345', 'temperature': 25, 'humidity': 60}"

s3 .put_object (Bucket =bucket_name ,Key =object_key ,Body =iot_data )