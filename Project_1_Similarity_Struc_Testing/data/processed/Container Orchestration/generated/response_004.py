import os
import subprocess
import yaml
from kubernetes import client ,config
from kubernetes .client import Configuration

def load_kubernetes_config ():
    try :
        config .load_kube_config ()
    except config .ConfigException :
        try :
            config .load_incluster_config ()
        except config .ConfigException :
            print ("Could not load Kubernetes configuration.")
            return None
    return client .NetworkingV1Api ()

def apply_network_policy (api_instance ,namespace ,policy ):
    try :
        api_instance .create_namespaced_network_policy (namespace ,policy )
        print ("Network policy applied successfully.")
    except client .ApiException as e :
        print (f"Error applying network policy: {e}")

def define_network_policy (namespace ):
    policy ={
    "apiVersion":"networking.k8s.io/v1",
    "kind":"NetworkPolicy",
    "metadata":{
    "name":"restrict-traffic",
    "namespace":namespace
    },
    "spec":{
    "podSelector":{},
    "policyTypes":["Ingress","Egress"],
    "ingress":[
    {
    "from":[
    {
    "podSelector":{
    "matchLabels":{
    "role":"backend"
    }
    }
    }
    ],
    "ports":[
    {
    "protocol":"TCP",
    "port":80
    }
    ]
    }
    ],
    "egress":[
    {
    "to":[
    {
    "podSelector":{
    "matchLabels":{
    "role":"database"
    }
    }
    }
    ],
    "ports":[
    {
    "protocol":"TCP",
    "port":5432
    }
    ]
    }
    ]
    }
    }
    return policy

def implement_rbac (namespace ):

    role ={
    "apiVersion":"rbac.authorization.k8s.io/v1",
    "kind":"Role",
    "metadata":{
    "namespace":namespace ,
    "name":"pod-reader"
    },
    "rules":[
    {
    "apiGroups":[""],
    "resources":["pods"],
    "verbs":["get","list","watch"]
    }
    ]
    }

    role_binding ={
    "apiVersion":"rbac.authorization.k8s.io/v1",
    "kind":"RoleBinding",
    "metadata":{
    "name":"read-pods",
    "namespace":namespace
    },
    "subjects":[
    {
    "kind":"User",
    "name":"jane-doe",
    "apiGroup":"rbac.authorization.k8s.io"
    }
    ],
    "roleRef":{
    "kind":"Role",
    "name":"pod-reader",
    "apiGroup":"rbac.authorization.k8s.io"
    }
    }

    return role ,role_binding

def apply_rbac (api_instance ,namespace ,role ,role_binding ):
    try :
        api_instance .create_namespaced_role (namespace ,role )
        api_instance .create_namespaced_role_binding (namespace ,role_binding )
        print ("RBAC applied successfully.")
    except client .ApiException as e :
        print (f"Error applying RBAC: {e}")

def enable_vulnerability_scanning (image ):
    try :
        subprocess .run (["trivy","image",image ])
    except FileNotFoundError :
        print ("Trivy not installed. Please install Trivy to enable vulnerability scanning.")
    except subprocess .CalledProcessError as e :
        print (f"Error running Trivy: {e}")

def main ():
    namespace ="your-namespace"
    image ="your-image:latest"

    api_instance =load_kubernetes_config ()
    if api_instance is None :
        return

    policy =define_network_policy (namespace )
    apply_network_policy (api_instance ,namespace ,policy )

    role ,role_binding =implement_rbac (namespace )
    apply_rbac (api_instance ,namespace ,role ,role_binding )

    enable_vulnerability_scanning (image )

if __name__ =="__main__":
    main ()