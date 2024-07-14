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

In the [previous blog](../fastapi), I mentioned how I was able to make simple endpoints with FastAPI and how I was even able to use it to deploy a pretrained ML model. Moving forward, I will be discussing about how to make our FastAPI application more robust and efficient with some commonly used practices I found around the internet. Note that these are completely optional and for just deploying a model, even the previous blog will suffice. It's just that I thought while I am at it, might just learn a bit more the best practices regarding FastAPI.

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
# Pydantic models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

# OAuth2 scheme using JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Function to verify JWT token and extract user information
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token_data = {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token_data

# Route to generate JWT token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if user_dict and form_data.password == "fakepassword":
        # Generate JWT token
        expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
        token_data = {"sub": form_data.username, "exp": expiration}
        token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

# Example protected route
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(verify_token)):
    return fake_users_db[current_user["username"]]
```

- **User Database:** Here, `fake_users_db` simulates a user database with a single user for demonstration.
- **Pydantic models:** `User` and `UserInDB` are Pydantic models used for type checking.
- **OAuth2 Scheme:** `oauth2_scheme` is configured using `OAuth2PasswordBearer`, specifying the token URL `(/token)` for token retrieval.
- **Token Verification:** `verify_token` function is a dependency that verifies and decodes the JWT token sent in the Authorization header of requests.
- **Token Generation:** The `/token` endpoint (login function) handles user authentication. If the credentials are valid (fakepassword is the hardcoded password for demonstration), it generates a JWT token using jwt.encode.
- **Protected Route:** The `/users/me` endpoint (read_users_me function) demonstrates a protected route that requires JWT token authentication (verify_token dependency). It returns user information based on the decoded JWT token and remains protected if try to access it without logging in or logging in with some other username or password.

Now, if open up `Swagger UI`, and try to access the `/users/me` endpoint, it won't show anything and give an error message saying we are not authenticated.

![Unautorized access](unauthorized.png)

However, if we login (Use `Autheticate` at the top right hand side of Swagger) with the credentials, `johndoe` and `fakepasword`, we are able to generate our JWT token and thus are logged in and can now access our protected endpoint.

![Authorized Access](authorized.png)

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
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app code into the container
COPY . /app/

# Expose the port that FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

2. Add a `requirements.txt` file in the FastAPI directory
```requirements.txt
fastapi
uvicorn
pyjwt
prometheus-client
```

2. **Build Docker Image:** Build the docker image
```bash
docker build -t my-fastapi-app .
```

3. **Run Docker Container:** Run the Docker container.
```bash
docker run -d --name my-fastapi-container -p 8000:8000 my-fastapi-app
```

4. The container should run without any issue and we can even monitor its health using:
```bash
sudo docker logs my-fastapi-container
```

![Running Docker Container](docker.png)

5. To stop the container use:
```bash
docker stop my-fastapi-container
```

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
    async def dispatch(self, request : Response, call_next):
        start_time = time.time()
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        except HTTPException as http_exc:
            # Capture HTTPException to get status_code
            status_code = http_exc.status_code
            raise http_exc

        finally:
            REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, status_code=status_code).inc()
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(latency)

app.add_middleware(PrometheusMiddleware)

@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

![FastAPI Metrics](metrics.png)

After this, we will be able to access our FastAPI metrics at the given endpoint. However, in order to understand it more efficiently, one can even use services like `Prometheus` and `Grafana`

## Conclusion
And that's a wrap. Phewww.. While there is a lot to cover in FastAPI and certainly it can't be done in a single blog, I still attempted to atleast log some of the things which I learnt during this time of learning FastAPI. After all, this is not a book lol. Just a reference blog for me to look back to when I get stuck with something working with FastAPI again. I think it covers most of the basic stuff and just in case I missed out something, I can always go back and have a look at the FastAPI docs. For now, I'd say that FastAPI is truly amazing as for how easy it is to make and manage endpoints and deploying my ML apps to it. And the best part? It's fairly easy to learn too. It took me just 2 days to go through all this and I believe someone who works with Python will find it fairly easy to use. With that being said, I think that's all from my side regarding FastAPI for now. Until Next Time. Adios!

## Appendix
- [Code for this blog](main.py)
- [Dockerfile Code](Dockerfile)
- [GitHub Actions Code](fastapi.yaml)

> Photo by [Data Scientist](https://datascientest.com/en/fastapi-everything-you-need-to-know-about-the-most-widely-used-python-web-framework-for-machine-learning)