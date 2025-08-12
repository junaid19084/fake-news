# Fake News Detection System

This project provides a system for detecting fake news using machine learning. It consists of:
- A FastAPI backend with an ML model
- A React frontend
- MongoDB for data storage
- Kubernetes deployment configuration
- CI/CD pipeline using GitHub Actions
- Nginx for load balancing

## Local Development

### Using Docker Compose

The easiest way to run this project locally is with Docker Compose:

```bash
# Run with locally built images
docker compose up -d

# OR run with images from Docker Hub (replace YOUR_DOCKERHUB_USERNAME)
DOCKERHUB_USERNAME=YOUR_DOCKERHUB_USERNAME docker compose up -d
```

Services will be available at:
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- MongoDB: localhost:27017

### Running Services Individually

#### MongoDB
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

#### Backend
```bash
cd fake-news/detector-ml
pip install -r requirement.txt
export MONGO_URI="mongodb://localhost:27017"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd fake-news/fake-news-ui
npm install
npm start
```

## Production Deployment

### Push Images to Docker Hub

```bash
./push-to-dockerhub.sh YOUR_DOCKERHUB_USERNAME
```

### Deploy to Kubernetes

```bash
./deploy.sh YOUR_DOCKERHUB_USERNAME
```

### GitHub Actions CI/CD Pipeline

The project includes a GitHub Actions workflow that will:
1. Build Docker images on push to main/master
2. Push images to Docker Hub
3. Deploy to Kubernetes (if configured)

To use it, set up the following GitHub secrets:
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Your Docker Hub access token
- `KUBE_CONFIG`: Your Kubernetes configuration file (base64 encoded)

## API Documentation

The API documentation is available at http://localhost:8000/docs when running the backend locally.

## Project Structure

```
fake-news/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── fake-news/
│   ├── detector-ml/          # ML backend
│   │   ├── app/
│   │   ├── dataset/
│   │   ├── model/
│   │   ├── Dockerfile
│   │   └── requirement.txt
│   └── fake-news-ui/         # React frontend
│       ├── public/
│       ├── src/
│       ├── Dockerfile
│       └── package.json
├── k8s/                      # Kubernetes configuration
│   ├── detector-ml-deployment.yaml
│   ├── fake-news-ui-deployment.yaml
│   ├── ingress.yaml
│   ├── mongodb-deployment.yaml
│   └── namespace.yaml
├── nginx/                    # Nginx configuration
│   └── nginx.conf
├── docker-compose.yml
├── deploy.sh
└── push-to-dockerhub.sh
```
