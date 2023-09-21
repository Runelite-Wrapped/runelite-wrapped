# Must be run from the root of the repo

sudo docker login

IMAGE=jerome3o/analytics
TAG=0.0.1

sudo docker build -t $IMAGE:$TAG -f docker/analytics/Dockerfile .
sudo docker tag $IMAGE:$TAG $IMAGE:latest

sudo docker push $IMAGE:$TAG
sudo docker push $IMAGE:latest
