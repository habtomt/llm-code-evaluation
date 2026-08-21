from pyspark .sql import SparkSession
from pyspark .streaming import StreamingContext
from pyspark .streaming .kafka import KafkaUtils
import json
from pyspark import SparkFiles

spark =SparkSession .builder .appName ("RealTimeEventProcessing").getOrCreate ()

ssc =StreamingContext (spark .sparkContext ,10 )

kafka_servers ="localhost:9092"
topic ="my_topic"

kafka_stream =KafkaUtils .createDirectStream (
ssc ,
[topic ],
kafka_servers ,
fromOffsets =None ,
keyDecoder ="json.loads",
valueDecoder ="json.loads",
)

def process_event (event ):

    data =json .loads (event [1 ])

    transformed_data ={"processed":data ["data"]+"_transformed"}

    return json .dumps (transformed_data )

processed_stream =kafka_stream .map (lambda x :process_event (x ))

producer =spark ._jvm .org .apache .spark .streaming .kafka .KafkaProducer (
"localhost:9092","output_topic"
)

processed_stream .foreachRDD (lambda rdd :rdd .saveAsTextFile ("output_topic"))

ssc .start ()

ssc .awaitTermination ()