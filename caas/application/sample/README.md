# Dockerコンテナ作成実習用

```
cd sample

# read config
view Dockerfile

# build image
sudo docker build ./ -t apache:1.0
sudo docker images

# start container
sudo docker run --name apache -itd -p 80:80 apache:1.0
sudo docker ps

# test
curl localhost

# stop container
sudo docker stop $(sudo docker ps -q)
```