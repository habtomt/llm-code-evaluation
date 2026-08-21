`python

from datetime import datetime

from vercel .serverless import serverless_function

@serverless_function

def process_real_time_data (event ,context ):

    processed_data =event .get ('data')

    transformed_data =apply_transformations (processed_data )

    current_timestamp =datetime .now ().strftime ("%Y-%m-%d %H:%M:%S")

    print (f"Processed data at {current_timestamp}: {transformed_data}")

    return transformed_data

def apply_transformations (data ):

    transformed_data =data .upper ()

    return transformed_data