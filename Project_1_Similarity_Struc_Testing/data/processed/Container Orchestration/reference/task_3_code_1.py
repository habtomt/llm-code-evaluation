from kubernetes import client ,config
from kubernetes .client .rest import ApiException
from kubernetes .client .models import V1Pod ,V1ObjectMeta ,V1Container ,V1PodSpec ,V1PodTemplateSpec ,V1LabelSelector ,V1Deployment ,V1DeploymentSpec

config .load_kube_config ()

api_instance =client .AppsV1Api ()

deployment =V1Deployment (
api_version ="apps/v1",
kind ="Deployment",
metadata =V1ObjectMeta (name ="example-deployment"),
spec =V1DeploymentSpec (
replicas =3 ,
selector =V1LabelSelector (match_labels ={"app":"example"}),
template =V1PodTemplateSpec (
metadata =V1ObjectMeta (labels ={"app":"example"}),
spec =V1PodSpec (
containers =[
V1Container (
name ="example-container",
image ="example-image:latest",
ports =[client .V1ContainerPort (container_port =80 )]
)
]
)
)
)
)

try :
    api_response =api_instance .create_namespaced_deployment (
    body =deployment ,
    namespace ="default"
    )
    print ("Deployment created. Status='%s'"%str (api_response .status ))
except ApiException as e :
    print ("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n"%e )