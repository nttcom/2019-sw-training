## Docker Image作成
```
cd app/backend/

# read script
view Dockerfile

# create image
sudo docker build ./ -t backend:1.0
# list images
sudo docker images

# build container
sudo docker run --name backend -itd -e MYSQL_IP=$HOST_IP -p 9200:9200 backend:1.0
# list conteiners
sudo docker ps

# test
curl localhost:9200/tasks
curl -XPOST -H "Content-Type: application/json" -d '{"item":"test"}' localhost:9200/tasks
curl localhost:9200/tasks/1
curl -XDELETE localhost:9200/tasks/1
curl -XPUT -H "Content-Type: application/json" -d '{"id":1, "item":"Training Preps #1_new", "is_done":true}' localhost:9200/tasks/1
curl localhost:9200/initialize
```


## Container Registryにpush
```
# attach GCP tag
sudo docker tag backend:1.0 asia.gcr.io/$PROJECT/backend-$NAME:1.0
# list images
sudo docker images

# push Container Registory
sudo gcloud docker -- push asia.gcr.io/$PROJECT/backend-$NAME:1.0
```


## GKE作成
```
# get clusters
gcloud container clusters list
# get nodes
kubectl get nodes
# get current cluster
kubectl config view -o jsonpath='{.contexts[*].name}'

# create deployment(pods)
envsubst < backend-deployment.yaml | kubectl create -f -
# get deployments
kubectl get deployments
# get pods
kubectl get pods

# create service
envsubst < backend-service.yaml | kubectl create -f -
# list services
kubectl get services

# get internal IP
kubectl get svc backend-$NAME-service -o=jsonpath="{.spec.clusterIP}"
# get external IP
kubectl get svc backend-$NAME-service -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"

#set environment variables
export IN_BACKEND_IP=`kubectl get svc backend-$NAME-service -o=jsonpath="{.spec.clusterIP}"`
export EX_BACKEND_IP=`kubectl get svc backend-$NAME-service -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"`

# test
curl $EX_BACKEND_IP:9200/tasks
curl -XPOST -H "Content-Type: application/json" -d '{"item":"test"}' $EX_BACKEND_IP:9200/tasks
```