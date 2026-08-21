from kubernetes import client, config



# Load Kubernetes configuration

config.load_kube_config()



# Create a Kubernetes client

api_instance = client.AppsV1Api()



# Define deployment metadata

metadata = client.V1ObjectMeta(name="example-deployment")

# Define container template

container = client.V1Container(name="example-container", image="example-image")

# Define pod template

template = client.V1PodTemplateSpec(metadata=metadata, spec=client.V1PodSpec(containers=[container]))



# Define deployment spec

spec = client.AppsV1DeploymentSpec(replicas=3, selector=client.V1LabelSelector(match_labels={"app": "example-app"}), template=template)



# Define deployment

deployment = client.AppsV1Deployment(metadata=metadata, spec=spec)



# Create deployment

api_instance.create_namespaced_deployment(namespace="default", body=deployment)