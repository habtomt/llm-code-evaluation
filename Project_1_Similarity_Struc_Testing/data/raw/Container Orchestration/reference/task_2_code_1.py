import kubernetes.client

from kubernetes.client.rest import ApiException

from kubernetes import client, config



def create_deployment_object():

    container = client.V1Container(

        name="my-container",

        image="my-image",

        resources=client.V1ResourceRequirements(

            requests={"cpu": "200m", "memory": "512Mi"},

            limits={"cpu": "500m", "memory": "1Gi"}

        )

    )



    template = client.V1PodTemplateSpec(

        metadata=client.V1ObjectMeta(labels={"app": "my-app"}),

        spec=client.V1PodSpec(containers=[container])

    )



    spec = client.V1DeploymentSpec(

        replicas=1,

        selector=client.V1LabelSelector(

            match_labels={"app": "my-app"}

        ),

        template=template

    )



    deployment = client.V1Deployment(

        api_version="apps/v1",

        kind="Deployment",

        metadata=client.V1ObjectMeta(name="my-deployment"),

        spec=spec

    )



    return deployment



def create_deployment(api_instance, deployment):

    api_response = api_instance.create_namespaced_deployment(

        body=deployment,

        namespace="default"

    )

    print("Deployment created. status='%s'" % str(api_response.status))



def main():

    config.load_kube_config()

    apps_v1 = client.AppsV1Api()

    

    deployment = create_deployment_object()

    create_deployment(apps_v1, deployment)



if __name__ == '__main__':

    main()