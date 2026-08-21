`python



# Create an S3 client



# Define the bucket and object key for the IoT data

bucket_name = 'my-iot-data-bucket'

object_key = 'iot-device-stream-data.txt'



# Sample IoT data to be stored

iot_data = "{'device_id': '12345', 'temperature': 25, 'humidity': 60}"



# Upload IoT data to S3

s3.put_object(Bucket=bucket_name, Key=object_key, Body=iot_data)