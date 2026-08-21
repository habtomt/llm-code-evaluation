apiVersion :networking .k8s .io /v1

kind :NetworkPolicy

metadata

name :deny -ingress

spec

podSelector :{}

policyTypes

-Ingress

apiVersion :v1

kind :Pod

metadata

name :secure -pod

spec

containers

-name :secure -container

securityContext

runAsUser :1000

allowPrivilegeEscalation :false

readOnlyRootFilesystem :true

capabilities

drop

-ALL

apiVersion :rbac .authorization .k8s .io /v1

kind :Role

metadata

name :pod -reader

rules

-apiGroups :[""]

resources :["pods"]

verbs :["get","watch","list"]

apiVersion :rbac .authorization .k8s .io /v1

kind :RoleBinding

metadata

name :read -pods

subjects

-kind :User

name :jane

apiGroup :rbac .authorization .k8s .io

roleRef

kind :Role

name :pod -reader

apiGroup :rbac .authorization .k8s .io

apiVersion :v1

kind :Pod

metadata

name :vulnerability -scanner

spec

containers

-name :trivy

args :["nginx"]