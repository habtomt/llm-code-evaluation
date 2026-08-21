

import json

from flask import Flask, request, jsonify

import boto3

from botocore.exceptions import ClientError

app = Flask(__name__)



model_name = 'your_model_name'

runtime_client = boto3.client('sagemaker-runtime')



@app.route('/predict', methods=['POST'])

def predict():

    try:

        input_data = request.get_json()

        response = runtime_client.invoke_endpoint(EndpointName=model_name, Body=json.dumps(input_data), ContentType='application/json')

        result = json.loads(response['Body'].read().decode())

        return jsonify(result), 200



    except ClientError as e:

        error_message = json.loads(e.response['Body'].read().decode())

        return jsonify({'error': error_message}), 500



if __name__ == '__main__':

    app.run(debug=True)