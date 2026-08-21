from kubernetes import client ,config
from kubernetes .client .rest import ApiException

config .load_kube_config ()

networking_v1_api =client .NetworkingV1Api ()
rbac_authorization_v1_api =client .RbacAuthorizationV1Api ()

security_policy ={
"apiVersion":"networking.k8s.io/v1",
"kind":"NetworkPolicy",
"metadata":{
"name":"restrict-traffic"
},
"spec":{
"podSelector":{
"matchLabels":{
"app":"myapp"
}
},
"policyTypes":["Ingress"],
"ingress":[{
"from":[{
"ipBlock":{
"cidr":"192.168.1.0/24",
"except":["192.168.1.4/32"]
}
}]
}]
}
}

try :
    api_response =networking_v1_api .create_namespaced_network_policy ("default",security_policy )
    print ("Security policy created: %s"%api_response .metadata .name )
except ApiException as e :
    print ("Exception when creating security policy: %s\n"%e )

access_control ={
"apiVersion":"rbac.authorization.k8s.io/v1",
"kind":"RoleBinding",
"metadata":{
"name":"restrict-access"
},
"subjects":[{
"kind":"User",
"name":"developer",
"apiGroup":"rbac.authorization.k8s.io"
}],
"roleRef":{
"kind":"ClusterRole",
"name":"admin",
"apiGroup":"rbac.authorization.k8s.io"
}
}

try :
    api_response =rbac_authorization_v1_api .create_namespaced_role_binding ("default",access_control )
    print ("Access control created: %s"%api_response .metadata .name )
except ApiException as e :
    print ("Exception when creating access control: %s\n"%e )