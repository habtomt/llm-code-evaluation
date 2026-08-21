import kafka
from kafka import KafkaProducer ,KafkaConsumer
import json
import logging
from influxdb import InfluxDBClient
from datetime import datetime

logging .basicConfig (level =logging .INFO )

KAFKA_BOOTSTRAP_SERVER ='localhost:9092'
KAFKA_TOPIC ='iot-data'
KAFKA_PROCESSED_TOPIC ='processed-iot-data'

INFLUXDB_HOST ='localhost'
INFLUXDB_PORT =8086
INFLUXDB_DB ='iot_data'
INFLUXDB_USER ='your_username'
INFLUXDB_PASSWORD ='your_password'

def ingest_data (temperature ,humidity ):

    producer =KafkaProducer (bootstrap_servers =KAFKA_BOOTSTRAP_SERVER )
    data ={'temperature':temperature ,'humidity':humidity }
    producer .send (KAFKA_TOPIC ,json .dumps (data ).encode ('utf-8'))
    producer .flush ()

def process_data ():

    consumer =KafkaConsumer (KAFKA_TOPIC ,
    bootstrap_servers =KAFKA_BOOTSTRAP_SERVER ,
    auto_offset_reset ='earliest',
    enable_auto_commit =True )
    producer =KafkaProducer (bootstrap_servers =KAFKA_BOOTSTRAP_SERVER )

    for message in consumer :
        data =json .loads (message .value .decode ('utf-8'))
        processed_data ={'temperature':data ['temperature'],'humidity':data ['humidity']}
        logging .info (f"Received data: {processed_data}")

        if 'temperature'in processed_data :
            processed_data ['temperature']=(processed_data ['temperature']-32 )*5.0 /9.0

        producer .send (KAFKA_PROCESSED_TOPIC ,json .dumps (processed_data ).encode ('utf-8'))

def store_data (temperature ,humidity ):

    client =InfluxDBClient (host =INFLUXDB_HOST ,port =INFLUXDB_PORT ,username =INFLUXDB_USER ,password =INFLUXDB_PASSWORD )
    client .switch_database (INFLUXDB_DB )

    data =[
    {
    "measurement":"iot_sensor_data",
    "fields":{
    "temperature":temperature ,
    "humidity":humidity
    },
    "time":datetime .now ().isoformat (),
    "tags":{
    "device":"iot_device"
    }
    }
    ]

    client .write_points (data )

def main ():
    try :

        ingest_data (22.5 ,60 )

        process_data ()

        store_data (22.5 ,60 )
    except Exception as e :
        logging .error (f"Error: {e}")

if __name__ =="__main__":
    main ()