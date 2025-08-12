#!/bin/bash

# Exit on any error
set -e

# Check if Docker Hub username is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <dockerhub_username>"
  exit 1
fi

DOCKERHUB_USERNAME=$1

echo "=== Setting up fake news detection system with Docker Hub username: $DOCKERHUB_USERNAME ==="

# Update Kubernetes deployment files with Docker Hub username
sed -i "s/\${DOCKERHUB_USERNAME}/$DOCKERHUB_USERNAME/g" k8s/detector-ml-deployment.yaml
sed -i "s/\${DOCKERHUB_USERNAME}/$DOCKERHUB_USERNAME/g" k8s/fake-news-ui-deployment.yaml

# Apply Kubernetes resources
echo "=== Creating Kubernetes namespace ==="
kubectl apply -f k8s/namespace.yaml

echo "=== Deploying MongoDB ==="
kubectl apply -f k8s/mongodb-deployment.yaml

echo "=== Deploying ML Detector Backend ==="
kubectl apply -f k8s/detector-ml-deployment.yaml

echo "=== Deploying Frontend UI ==="
kubectl apply -f k8s/fake-news-ui-deployment.yaml

echo "=== Configuring Ingress ==="
kubectl apply -f k8s/ingress.yaml

echo "=== Deployment Complete ==="
echo "Waiting for pods to be ready..."
sleep 5

kubectl get pods -n fake-news

echo ""
echo "Add the following entry to your /etc/hosts file to access the application:"
echo "127.0.0.1 fake-news.example.com"
echo ""
echo "Then access the application at: http://fake-news.example.com"
