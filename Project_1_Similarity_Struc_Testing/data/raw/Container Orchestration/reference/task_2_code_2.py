import kubernetes.client

from kubernetes.client.rest import ApiException

from kubernetes import config



# Load Kubernetes config from default location

config.load_kube_config()



# Create Kubernetes API client

api_instance = kubernetes.client.CoreV1Api()



# Specify the pod name and namespace

name = 'example-pod'

namespace = 'default'



try:

    api_response = api_instance.read_namespaced_pod(name, namespace)

    

    # Update pod's resource limits and requests

    api_response.spec.containers[0].resources.limits = {'cpu': '200m', 'memory': '512Mi'}

    api_response.spec.containers[0].resources.requests = {'cpu': '100m', 'memory': '256Mi'}

    

    # Apply changes to the pod

    api_instance.replace_namespaced_pod(name, namespace, api_response)

    print("Pod resources updated successfully.")



except ApiException as e:

    print("Exception when calling CoreV1Api->read_namespaced_pod: %s\n" % e)