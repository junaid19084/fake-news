#!/bin/bash

# Exit on any error
set -e

# Check if Docker Hub username is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dockerhub_username>"
  exit 1
fi

DOCKERHUB_USERNAME=$1

echo "=== Building and pushing Docker images to Docker Hub username: $DOCKERHUB_USERNAME ==="

# Build and push detector-ml
echo "=== Building and pushing detector-ml ==="
docker build -t $DOCKERHUB_USERNAME/fake-news-detector-ml:latest ./fake-news/detector-ml
docker push $DOCKERHUB_USERNAME/fake-news-detector-ml:latest

# Build and push fake-news-ui
echo "=== Building and pushing fake-news-ui ==="
docker build -t $DOCKERHUB_USERNAME/fake-news-ui:latest ./fake-news/fake-news-ui
docker push $DOCKERHUB_USERNAME/fake-news-ui:latest

echo "=== Images successfully pushed to Docker Hub ==="
echo "You can now use these images in your Kubernetes deployment with:"
echo "./deploy.sh $DOCKERHUB_USERNAME"
