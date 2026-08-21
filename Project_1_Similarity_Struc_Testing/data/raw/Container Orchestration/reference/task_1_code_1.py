# Scenario 2: High Availability Setup

import kubernetes.client

from kubernetes import client, config



# Load the Kubernetes configuration from default location

config.load_kube_config()



# Define container

container = client.V1Container(name="high-availability-container", image="nginx")



# Create a deployment object and configure redundant and distributed container instances

deployment = client.V1Deployment(api_version="apps/v1", kind="Deployment", metadata=client.V1ObjectMeta(name="high-availability-deployment"))

spec = client.V1DeploymentSpec(replicas=3, selector=client.V1LabelSelector(match_labels={"app": "high-availability-app"}))



# Configure pod template

template = client.V1PodTemplateSpec(metadata=client.V1ObjectMeta(labels={"app": "high-availability-app"}))

template.spec = client.V1PodSpec(containers=[container])

spec.template = template

deployment.spec = spec



# Apply the deployment

apps_v1 = client.AppsV1Api()

apps_v1.create_namespaced_deployment(namespace="default", body=deployment)