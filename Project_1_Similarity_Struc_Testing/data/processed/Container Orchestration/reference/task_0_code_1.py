from kubernetes import client ,config

config .load_kube_config ()

api_instance =client .AppsV1Api ()

metadata =client .V1ObjectMeta (name ="example-deployment")

container =client .V1Container (name ="example-container",image ="example-image")

template =client .V1PodTemplateSpec (metadata =metadata ,spec =client .V1PodSpec (containers =[container ]))

spec =client .AppsV1DeploymentSpec (replicas =3 ,selector =client .V1LabelSelector (match_labels ={"app":"example-app"}),template =template )

deployment =client .AppsV1Deployment (metadata =metadata ,spec =spec )

api_instance .create_namespaced_deployment (namespace ="default",body =deployment )