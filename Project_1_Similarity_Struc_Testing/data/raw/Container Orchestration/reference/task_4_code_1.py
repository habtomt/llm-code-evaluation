

# Security Enforcement using Kubernetes



# 1. Define Network Policy

apiVersion: networking.k8s.io/v1

kind: NetworkPolicy

metadata

name: deny-ingress

spec

podSelector: {}

policyTypes

- Ingress



# 2. Define Security Context for Pods

apiVersion: v1

kind: Pod

metadata

name: secure-pod

spec

containers

- name: secure-container

securityContext

runAsUser: 1000

allowPrivilegeEscalation: false

readOnlyRootFilesystem: true

capabilities

drop

- ALL



# 3. Set up Role-Based Access Control

apiVersion: rbac.authorization.k8s.io/v1

kind: Role

metadata

name: pod-reader

rules

- apiGroups: [""]

resources: ["pods"]

verbs: ["get", "watch", "list"]



apiVersion: rbac.authorization.k8s.io/v1

kind: RoleBinding

metadata

name: read-pods

subjects

- kind: User

name: jane

apiGroup: rbac.authorization.k8s.io

roleRef

kind: Role

name: pod-reader

apiGroup: rbac.authorization.k8s.io



# 4. Implement Vulnerability Scanning

apiVersion: v1

kind: Pod

metadata

name: vulnerability-scanner

spec

containers

- name: trivy

args: ["nginx"]