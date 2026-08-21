import os
import sys
from kubernetes import client ,config
from docker import Client
import github
from github import Github

def setup_kubernetes ():
    try :

        config .load_kube_config ()
        return client .AppsV1Api ()
    except Exception as e :
        print (f"Error setting up Kubernetes: {e}")
        sys .exit (1 )

def setup_docker ():
    try :

        return Client (base_url ='unix://var/run/docker.sock')
    except Exception as e :
        print (f"Error setting up Docker: {e}")
        sys .exit (1 )

def setup_github (token ):
    try :

        return Github (token )
    except Exception as e :
        print (f"Error setting up GitHub: {e}")
        sys .exit (1 )

def build_and_push_image (docker_client ,image_name ,tag ):
    try :

        docker_client .build (path ='.',tag =f"{image_name}:{tag}")

        docker_client .push (f"{image_name}:{tag}")
    except Exception as e :
        print (f"Error building and pushing Docker image: {e}")
        sys .exit (1 )

def deploy_to_kubernetes (kubernetes_client ,deployment_name ,image_name ,tag ):
    try :

        kubernetes_client .patch_namespaced_deployment (
        name =deployment_name ,
        namespace ='default',
        body ={
        'spec':{
        'template':{
        'spec':{
        'containers':[
        {
        'name':deployment_name ,
        'image':f"{image_name}:{tag}"
        }
        ]
        }
        }
        }
        }
        )
    except Exception as e :
        print (f"Error deploying to Kubernetes: {e}")
        sys .exit (1 )

def main ():

    kubernetes_client =setup_kubernetes ()

    docker_client =setup_docker ()

    github_token =os .environ .get ('GITHUB_TOKEN')
    github_client =setup_github (github_token )

    repository =github_client .get_repo ('your-repo/your-repo')
    branch ='main'

    image_name ='your-image'
    tag ='latest'
    build_and_push_image (docker_client ,image_name ,tag )

    deployment_name ='your-deployment'
    deploy_to_kubernetes (kubernetes_client ,deployment_name ,image_name ,tag )

if __name__ =='__main__':
    main ()