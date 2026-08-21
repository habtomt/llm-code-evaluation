docker build -t gcr.io/my-project/my-model .

docker push gcr.io/my-project/my-model

gcloud container clusters create my-cluster

gcloud container clusters get-credentials my-cluster

kubectl create deployment my-deployment --image=gcr.io/my-project/my-model

kubectl expose deployment my-deployment --type=LoadBalancer --port=80 --target-port=8080

kubectl autoscale deployment my-deployment --min=3 --max=10 --cpu-percent=75

gcloud services enable monitoring.googleapis.com

gcloud services enable container.googleapis.com