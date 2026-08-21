import json
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
import boto3

app = Flask(__name__)

sagemaker_client = boto3.client('sagemaker-runtime', region_name='<your-region>')  # Replace <your-region>

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        response = sagemaker_client.invoke_endpoint(
            EndpointName='<your-endpoint-name>',  # Replace <your-endpoint-name>
            Body=json.dumps(data),
            ContentType='application/json'
        )
        result = json.loads(response['Body'].read().decode())
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

executor = ThreadPoolExecutor(10)

if __name__ == '__main__':
    app.run(debug=True)