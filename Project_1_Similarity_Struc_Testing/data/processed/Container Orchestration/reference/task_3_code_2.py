from kubernetes import client ,config
from kubernetes .client .rest import ApiException
from kubernetes import watch

def create_deployment ():

    apps_v1 =client .AppsV1Api ()
    deployment =client .V1Deployment (
    api_version ="apps/v1",
    kind ="Deployment",
    metadata =client .V1ObjectMeta (name ="example-deployment"),
    spec =client .V1DeploymentSpec (
    selector =client .V1LabelSelector (
    match_labels ={"app":"example"}
    ),
    replicas =3 ,
    template =client .V1PodTemplateSpec (
    metadata =client .V1ObjectMeta (labels ={"app":"example"}),
    spec =client .V1PodSpec (
    containers =[
    client .V1Container (
    name ="example",
    image ="example/image:latest",
    ports =[client .V1ContainerPort (container_port =80 )]
    )
    ]
    )
    )
    )
    )

    try :
        api_response =apps_v1 .create_namespaced_deployment (
        body =deployment ,
        namespace ="default"
        )
        print ("Deployment created. Status='%s'"%str (api_response .status ))
    except ApiException as e :
        print ("Exception when calling AppsV1Api->create_namespaced_deployment: %s\n"%e )

def main ():
    config .load_kube_config ()
    create_deployment ()

if __name__ =="__main__":
    main ()