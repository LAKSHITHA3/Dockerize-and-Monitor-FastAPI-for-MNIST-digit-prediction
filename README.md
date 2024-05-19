# MNIST Digit Classifier with Monitoring

This project demonstrates a FastAPI application for MNIST digit classification, integrated with Prometheus for monitoring and Grafana for visualization. The application can be containerized using Docker and deployed as a cluster for scalability.

## Features
- **FastAPI**: Serves the MNIST digit classification model.
- **Prometheus**: Collects metrics for monitoring the API.
- **Grafana**: Visualizes the metrics collected by Prometheus.
- **Docker**: Containerizes the entire application for easy deployment and scalability.

## Project Structure
```
mnist_digit_classifier/
│
├── Dockerfile
├── docker-compose.yml
├── main.py
├── prometheus.yml
├── requirements.txt
└── model/
    └── mnist_model.h5
```

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose
- Python 3.9 or later

### Step-by-Step Setup

#### 1. Clone the Repository
```sh
git clone <your-repository-url>
cd mnist_digit_classifier
```

#### 2. Prepare the Model
Ensure you have your trained MNIST model saved as `mnist_model.h5` in the `model` directory.

#### 3. Build and Run Docker Containers
```sh
docker-compose up --build
```

#### 4. Access the Services
- **FastAPI**: `http://localhost:8000`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3000` (default credentials: `admin/admin`)

#### 5. Configure Grafana
1. Log in to Grafana at `http://localhost:3000`.
2. Add Prometheus as a data source:
   - URL: `http://prometheus:9090`
3. Create dashboards to visualize your metrics.

### Testing the API
You can test the API using Swagger UI or tools like Postman or curl.

#### Using Swagger UI
1. Open `http://localhost:8000/docs` in your browser.
2. Use the `/predict` endpoint to upload a 28x28 image of a digit and get the prediction.

#### Using curl
```sh
curl -X POST "http://localhost:8000/predict" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@path_to_your_image"
```

## Prometheus Metrics
- **Total Number of Requests**: Counts the total number of requests received.
- **Latency of Requests**: Measures the latency of each request.
- **Effective Processing Time**: Measures the effective processing time per character.

## Grafana Dashboard
![Grafana Dashboard](./screenshots/grafana_dashboard.png)

## Scaling with Multiple Instances
To run multiple instances of the FastAPI application, update the `docker-compose.yml` file to deploy replicas:

```yaml
services:
  fastapi:
    build: .
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=model/mnist_model.h5
```

Run the containers again:

```sh
docker-compose up --build
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
