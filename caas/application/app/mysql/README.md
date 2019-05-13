## Docker Image作成
```
cd app/mysql/

# read script
view Dockerfile

# create image
sudo docker build ./ -t mysql:1.0
# list images
sudo docker images

# build container
sudo docker run --name mysql -itd -p 3306:3306 mysql:1.0
# list conteiners
sudo docker ps

# test
mysql -h127.0.0.1 -uuser -ppassword
```

## Container Registryにpush
```
# attach GCP tag
sudo docker tag mysql:1.0 asia.gcr.io/$PROJECT/mysql-$NAME:1.0
# list images
sudo docker images

# push Container Registory
sudo gcloud docker -- push asia.gcr.io/$PROJECT/mysql-$NAME:1.0
```

## GKE作成
```
# create cluster(nodes)
gcloud container clusters create --num-nodes=2 caas-${NAME} --region asia-northeast1 --machine-type g1-small --enable-autoscaling --min-nodes=2 --max-nodes=3
# get clusters
gcloud container clusters list
# get nodes
kubectl get nodes
# get current cluster
kubectl config view -o jsonpath='{.contexts[*].name}'

# create deployment(pods)
envsubst < mysql-deployment.yaml | kubectl create -f -
# get deployments
kubectl get deployments
# get pods
kubectl get pods

# create service
envsubst < mysql-service.yaml | kubectl create -f -

# list services
kubectl get services

# get internal IP
kubectl get svc mysql-$NAME-service -o=jsonpath="{.spec.clusterIP}"
# get external IP
kubectl get svc mysql-$NAME-service -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"

#set environment variables
export IN_MYSQL_IP=`kubectl get svc mysql-$NAME-service -o=jsonpath="{.spec.clusterIP}"`
export EX_MYSQL_IP=`kubectl get svc mysql-$NAME-service -o=jsonpath="{.status.loadBalancer.ingress[0].ip}"`

# test
mysql -h$EX_MYSQL_IP -uuser -ppassword
```