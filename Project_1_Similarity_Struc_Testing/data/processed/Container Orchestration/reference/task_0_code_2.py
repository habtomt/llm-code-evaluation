from kubernetes import client ,config

from kubernetes .client .rest import ApiException

def create_deployment (name ,image ,replicas ):

    config .load_kube_config ()

    apps_v1 =client .AppsV1Api ()

    deploy =client .V1Deployment ()

    deploy .metadata =client .V1ObjectMeta (name =name )

    deploy .spec =client .V1DeploymentSpec (

    replicas =replicas ,

    selector =client .V1LabelSelector (

    match_labels ={"app":name }

    ),

    template =client .V1PodTemplateSpec (

    metadata =client .V1ObjectMeta (labels ={"app":name }),

    spec =client .V1PodSpec (

    containers =[

    client .V1Container (

    name =name ,

    image =image

    )

    ]

    )

    )

    )

    try :

        apps_v1 .create_namespaced_deployment (namespace ="default",body =deploy )

        print (f"Deployment {name} created successfully")

    except ApiException as e :

        print (f"Exception when creating deployment: {e}")

create_deployment ("my-app","my-image:latest",3 )