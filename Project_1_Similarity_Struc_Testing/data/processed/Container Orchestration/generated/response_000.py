import os
import subprocess
import yaml
from kubernetes import client ,config

RANCHER_SERVER_IP ='YOUR_RANCHER_SERVER_IP'
RANCHER_USERNAME ='YOUR_RANCHER_USERNAME'
RANCHER_PASSWORD ='YOUR_RANCHER_PASSWORD'
KUBERNETES_CONFIG_FILE ='YOUR_KUBERNETES_CONFIG_FILE'

def install_rancher ():
    try :

        subprocess .run (['sudo','curl','-fsSL','https://get.docker.com','|','sh'])
        subprocess .run (['sudo','systemctl','start','docker'])
        subprocess .run (['sudo','systemctl','enable','docker'])

        subprocess .run (['docker','run','-d','--restart=unless-stopped','-p','80:80','-p','443:443','rancher/rancher'])
    except Exception as e :
        print (f"Error installing Rancher: {e}")

def add_kubernetes_cluster (cluster_name ,cluster_config ):
    try :

        rancher_config =client .Configuration ()
        rancher_config .host =f'https://{RANCHER_SERVER_IP}'
        rancher_config .username =RANCHER_USERNAME
        rancher_config .password =RANCHER_PASSWORD

        rancher_client =client .ApiClient (rancher_config )

        cluster =client .Cluster (
        name =cluster_name ,
        spec =client .ClusterSpec (
        rancher_kubernetes_engine_config =client .RancherKubernetesEngineConfig (

        config_file =KUBERNETES_CONFIG_FILE
        )
        )
        )

        client .ClusterApi (rancher_client ).create (cluster )
    except Exception as e :
        print (f"Error adding Kubernetes cluster to Rancher: {e}")

def deploy_application (cluster_name ,application_config ):
    try :

        config .load_kube_config (KUBERNETES_CONFIG_FILE )

        kubernetes_client =client .ApiClient ()

        deployment =client .AppsV1Deployment (
        api_version ='apps/v1',
        kind ='Deployment',
        metadata =client .V1ObjectMeta (
        name ='nginx-deployment'
        ),
        spec =client .AppsV1DeploymentSpec (
        replicas =3 ,
        selector =client .V1LabelSelector (
        match_labels ={'app':'nginx'}
        ),
        template =client .V1PodTemplateSpec (
        metadata =client .V1ObjectMeta (
        labels ={'app':'nginx'}
        ),
        spec =client .V1PodSpec (
        containers =[
        client .V1Container (
        name ='nginx',
        image ='nginx:latest',
        ports =[client .V1ContainerPort (container_port =80 )]
        )
        ]
        )
        )
        )
        )

        client .AppsV1Api (kubernetes_client ).create_namespaced_deployment (
        namespace ='default',
        body =deployment
        )
    except Exception as e :
        print (f"Error deploying application: {e}")

def main ():

    install_rancher ()

    add_kubernetes_cluster ('my-cluster','path/to/cluster/config')

    deploy_application ('my-cluster','path/to/application/config')

if __name__ =='__main__':
    main ()