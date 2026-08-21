import os
import subprocess
import yaml

def containerize_with_docker (app_name ,port ):

    try :

        dockerfile =f"""
        # Use the official lightweight Node.js image
        FROM node:14-alpine

        # Set the working directory
        WORKDIR /usr/src/app

        # Copy package.json and package-lock.json
        COPY package*.json ./

        # Install dependencies
        RUN npm install

        # Bundle app source
        COPY . .

        # Expose the port the app runs on
        EXPOSE {port}

        # Run the application
        CMD ["node", "app.js"]
        """
        with open ("Dockerfile","w")as f :
            f .write (dockerfile )

        subprocess .run (["docker","build","-t",app_name ,"."])

        subprocess .run (["docker","run","-p",f"{port}:{port}",app_name ])
    except Exception as e :
        print (f"Error containerizing with Docker: {e}")

def prepare_for_kubernetes_deployment (app_name ,port ):

    try :

        deployment_yaml ={
        "apiVersion":"apps/v1",
        "kind":"Deployment",
        "metadata":{
        "name":f"{app_name}-deployment"
        },
        "spec":{
        "replicas":3 ,
        "selector":{
        "matchLabels":{
        "app":app_name
        }
        },
        "template":{
        "metadata":{
        "labels":{
        "app":app_name
        }
        },
        "spec":{
        "containers":[
        {
        "name":app_name ,
        "image":f"{app_name}:latest",
        "ports":[
        {
        "containerPort":port
        }
        ]
        }
        ]
        }
        }
        }
        }
        with open ("deployment.yaml","w")as f :
            yaml .dump (deployment_yaml ,f )

        service_yaml ={
        "apiVersion":"v1",
        "kind":"Service",
        "metadata":{
        "name":f"{app_name}-service"
        },
        "spec":{
        "type":"LoadBalancer",
        "selector":{
        "app":app_name
        },
        "ports":[
        {
        "protocol":"TCP",
        "port":80 ,
        "targetPort":port
        }
        ]
        }
        }
        with open ("service.yaml","w")as f :
            yaml .dump (service_yaml ,f )
    except Exception as e :
        print (f"Error preparing for Kubernetes deployment: {e}")

def deploy_to_kubernetes (app_name ):

    try :

        subprocess .run (["kubectl","apply","-f","deployment.yaml"])
        subprocess .run (["kubectl","apply","-f","service.yaml"])

        subprocess .run (["kubectl","get","pods"])
        subprocess .run (["kubectl","get","services"])
    except Exception as e :
        print (f"Error deploying to Kubernetes: {e}")

def scale_deployment (app_name ,replicas ):

    try :

        subprocess .run (["kubectl","scale","deployment",f"{app_name}-deployment","--replicas",str (replicas )])
    except Exception as e :
        print (f"Error scaling deployment: {e}")

def main ():
    app_name ="my-node-app"
    port =3000
    replicas =5

    containerize_with_docker (app_name ,port )

    prepare_for_kubernetes_deployment (app_name ,port )

    deploy_to_kubernetes (app_name )

    scale_deployment (app_name ,replicas )

if __name__ =="__main__":
    main ()