---
title: "Building Efficient ML APIs with FastAPI: A Comprehensive Guide - Part 2"
description: "FastAPI: Guide to building prototype ML applications quick and easy AF"
slug: fastapi2
date: 2024-07-13 00:00:00+0000
image: /blogs/fastapi/fastAPI.webp #Fixit 
license: false
categories:
    - Deployment
    - REST
tags:
    - Model Deployment
    - REST
    - API
    - FastAPI
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

## Advanced Features with FastAPI
After learning how to be able to serve my models using FastAPI, I decided to extend it further in order to enhance the functionality, security and scalability of my API. For this, I read about additional topics like input validation, error handling and authentication, which although won't be help me much for the purpose for which I initially started learning FastAPI, i.e., to make demo apps for my ML models, but they are crucial for developing production-ready APIs and so I thought about giving them a read too.

### Input Validation
Input validation ensures that incoming data meets specified criteria before processing. FastAPI integrates seamlessly with `Pydantic` for data validation, leveraging Python's type hints. Here’s how I implemented input validation in my FastAPI application:

```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name : str = Field(..., decription = "The name of the item")
    price : float = Field(..., gt = 0, decription = "The price of the item")

@app.post('/items/')
def create_item(item: Item):
    return {'name' : item.name, 'price' : item.price}
```

- **Explanation:** In this example, the `Item` Pydantic model specifies that `name` is a required string field and `price` is a required float field greater than 0. FastAPI automatically validates incoming requests against these criteria and returns appropriate error responses if validation fails.

### Error Handling
Error handling is crucial for providing informative responses when something goes wrong in an API request. FastAPI simplifies error handling with HTTPException and exception handling mechanisms. Here’s an example of handling errors in FastAPI which we've seen before too during CRUD operations.
```python
from fastapi import HTTPException

@app.get('items/{item_id}')
def read_item(item_id : int):
    if item_id not in range(1, 6):
        raise HTTPException(status_code = 404, detail = "Item not found")
    return {'item' : item_id}
```

- **Explanation:** In this example, if the `item_id` provided in the request path is not within the range of valid item IDs (1 to 5), FastAPI raises an `HTTPException` with a 404 status code and a detailed error message along with that.

### Authentication and Authorization
Securing APIs with authentication and authorization mechanisms is essential for protecting sensitive data and restricting access to authorized users. FastAPI supports various authentication methods, including OAuth2, JWT (JSON Web Tokens), and basic authentication. Here’s a simple example of implementing JWT authentication in FastAPI:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

security = OAuth2PasswordBearer(tokenurl='/token')

# Mock user database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$V2qBpWn5GDK/9QrF3l7AyO6x9BdFssEcVbOeYURVn8t62MzK4IO5u",  # hashed version of password 'secret'
        "disabled": False,
    }
}

def verify_password(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not password:
        return False
    if password == 'secret':
        return True


def get_current_user(token: str = Depends(security)):
    username, _ = token.split(":")
    user = fake_users_db.get(username)

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid Credentials',
            headers = {"WWW-Authenticate": "Bearer"}
        )   
    return user

@app.get('users/me')
def read_current_user(current_user : dict = Depends(get_current_user)):
    return current_user
```

- **Explanation:** In this example, `OAuth2PasswordBearer` is used to define an authentication scheme using OAuth2 with password flow. The `get_current_user()` function verifies the JWT token and retrieves the current user from the mock database `(fake_users_db)`. The `read_current_user()` endpoint demonstrates accessing user information with authentication.

## Deployment Strategies for FASTApi
Moving further, after building the app, it is also essential to be able to deploy it. FastAPI applications can be deployed using various deployment options, depending on scalability requirements, infrastructure preferences, and operational constraints. Here are some common deployment strategies.

- **Docker Containers:** Containerization with Docker allows packaging FastAPI applications and their dependencies into lightweight, portable containers. This approach facilitates consistent deployment across different environments and simplifies scaling.

- **Serverless Deployment:** Serverless platforms like AWS Lambda or Azure Functions offer auto-scaling and pay-per-use pricing models. FastAPI applications can be deployed as serverless functions, eliminating the need to manage infrastructure manually.

- **Traditional Servers:** Deploying FastAPI on traditional servers or virtual machines provides more control over infrastructure configuration and performance tuning. Platforms like AWS EC2, Google Compute Engine, or DigitalOcean Droplets are commonly used for this approach.

### Deployment Best Practices
When deploying FastAPI applications in production, consider the following best practices to ensure reliability, security, and scalability:


- **Environment Configuration:** Use environment variables for sensitive information (e.g., API keys, database credentials) and configuration settings (e.g., logging levels, debug mode).

- **Monitoring and Logging:** Implement monitoring solutions (e.g., Prometheus, Datadog) to track performance metrics, error rates, and application health. Centralized logging (e.g., ELK Stack, Splunk) helps in troubleshooting and debugging issues.

- **Security Measures:** Secure FastAPI applications with HTTPS/TLS encryption to protect data in transit. Implement authentication and authorization mechanisms (e.g., OAuth2, JWT) to control access to APIs and sensitive resources.

- **Scaling Strategies:** Plan for horizontal scaling by deploying multiple instances of FastAPI behind a load balancer to handle increased traffic. Use auto-scaling features offered by cloud providers for efficient resource utilization.

### Deployment with Docker
For my learning purposes, I did not go in depth but still learned how to containerize a FASTApi application using Docker atleast.

1. **Dockerfile:** Create a `Dockerfile` in your FastAPI project directory.
```Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./app /app
```

Replace `./app` with the path to your FastAPI application directory.

2. **Build Docker Image:** Build the docker image
```bash
docker build -t fastapi-app
```

3. **Run Docker Container:** Run the Docker container.
```bash
docker run -d -p 80:80 fastapi-app
```

Adjust `-p 80:80` to map the container port to a desired host port.

## Continuous Integration and Delivery (CI/CD) for FastAPI
Phewwww! Now that we've come all the way to deployment, I thought why not also add some CI/CD pipelines to it as it helps automate the building, testing and deployment processes, ensuring reliable and efficient software delivery.

### Setting up a CI/CD Pipeline
CI/CD pipelines automate several key tasks in the software development lifecycle, including:

- **Code Compilation:** Compile and package the FastAPI application.
- **Testing:** Execute automated tests to verify functionality and detect issues early.
- **Deployment:** Deploy the application to staging or production environments automatically.

### Example CI/CD Pipeline with GitHub Actions
Here's an example of setting up a CI/CD pipeline for FastAPI. I found this online and have yet to test it though.

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest --cov=app tests/

      - name: Build Docker image
        run: |
          docker build -t my-fastapi-app .
          docker tag my-fastapi-app:latest my-fastapi-app:$(git rev-parse --short $GITHUB_SHA)

      - name: Push Docker image to registry
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push Docker image
        run: docker push my-fastapi-app

      - name: Deploy to staging
        if: github.ref == 'refs/heads/main'
        run: |
          ssh user@staging-server 'docker pull my-fastapi-app:latest'
          ssh user@staging-server 'docker-compose up -d'
```

## Monitoring and Optimization for FastAPI
Last but not the least, it is equally important to monitor and log the metrics of our FastAPI application as building one as monitoring provides us with insights into application behaviour and performance metrics and also helps enhance efficiency and responsiveness.

### Monitoring Strategies
Effective monitoring helps identify issues, track performance metrics, and ensure the smooth operation of FastAPI applications. Consider the following monitoring strategies:

- **Logging:** Implement logging to record application events, errors, and debug information. Use structured logging for better analysis and troubleshooting.

- **Metrics Collection:** Monitor key performance indicators (KPIs) such as request/response times, error rates, and resource utilization (CPU, memory). Tools like Prometheus, DataDog, or AWS CloudWatch Metrics can be integrated for metrics collection.

- **Alerting:** Set up alerts based on predefined thresholds (e.g., high error rates, CPU utilization) to proactively address potential issues.

### Performace Optimization
Optimizing FastAPI applications improves efficiency and responsiveness, enhancing user experience and reducing operational costs. Consider the following optimization techniques:

- **Code Profiling:** Identify performance bottlenecks using profiling tools (e.g., cProfile) to analyze execution times and optimize critical sections of code.

- **AsyncIO:** Leverage FastAPI's asynchronous capabilities and AsyncIO to handle concurrent requests efficiently, especially for I/O-bound operations.

- **Caching:** Implement caching mechanisms (e.g., Redis, Memcached) to store and retrieve frequently accessed data, reducing database load and improving response times.

- **Database Optimization:** Optimize database queries with indexes, query optimization techniques, and connection pooling to enhance database performance.

### Adding Metrics to FastAPI
Integrate Prometheus for monitoring metrics in FastAPI:

1. Install Prometheus client
```bash
pip install prometheus-client
```

2. Add Metrics Middleware
```python
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter("request_count", "Total count of requests", ["method", "endpoint", "status_code"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])

class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        path = request.url.path
        method = request.method
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            REQUEST_COUNT.labels(method=method, endpoint=path, status_code=status_code).inc()
            latency = time.time() - request.scope["start_time"]
            REQUEST_LATENCY.labels(method=method, endpoint=path).observe(latency)

app.add_middleware(PrometheusMiddleware)
```

3. Expose Metrics Endpoint:
```python
from fastapi.responses import Response

@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

4. Instrument Endpoints:
```python
@app.get("/items/")
async def read_items():
    # Endpoint logic
    return {"message": "Items retrieved successfully"}
```

## Conclusion
And that's a wrap. Phewww.. While there is a lot to cover in FastAPI and certainly it can't be done in a single blog, I still attempted to atleast log some of the things which I learnt during this time of learning FastAPI. After all, this is not a book lol. Just a reference blog for me to look back to when I get stuck with something working with FastAPI again. I think it covers most of the basic stuff and just in case I missed out something, I can always go back and have a look at the FastAPI docs. For now, I'd say that FastAPI is truly amazing as for how easy it is to make and manage endpoints and deploying my ML apps to it. And the best part? It's fairly easy to learn too. It took me just 2 days to go through all this and I believe someone who works with Python will find it fairly easy to use. With that being said, I think that's all from my side regarding FastAPI for now. Until Next Time. Adios!