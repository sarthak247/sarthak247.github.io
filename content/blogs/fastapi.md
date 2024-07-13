---
title: "Building Efficient ML APIs with FastAPI: A Comprehensive Guide"
description: "FastAPI: Guide to building prototype ML applications quick and easy AF"
slug: fastapi
date: 2024-07-13 00:00:00+0000
image: /blogs/hello-world/cover.jpg #Fixit 
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

## Introduction to FastAPI
Today, I delved into FastAPI, a cutting-edge web framework designed for building APIs with Python. It piqued my interest because of its reputation for speed, ease of use, and robust integration with Python's type system and also cause I have been looking for some time for a way to deploy my ML applications easily and with minimalistic code as I'm not a web developer and struggle with that part. Upon looking around on the internet, I discovered that people have been using something called `FastAPI` along with `Streamlit` for faster model deployment for demonstration purposes and so I decided to have a look at it. Here’s what I discovered about FastAPI and why it's particularly compelling for developing APIs, especially for machine learning tasks.

### Exploring FastAPI
Well, in order to explore about FastAPI, I did what every other sane developer would do. I opened up YouTube and started looking at video tutorials along with looking at its documentation. I got to know that FastAPI uses `Starlette` for its web components and `Pydantic` for data validation and serialization, leveraging Python's type hints for seamless integration and enhanced development experience. (YIPPEEE! This also meant less learning for me as I could already use some of the things I knew from Python without the need to learn some completely different framework or language). Thus, I chose to explore it further.

### Advantages That Caught My Attention
- **Performance:** FastAPI harnesses asynchronous programming to handle high volumes of concurrent requests efficiently. This capability is crucial for applications that require real-time data processing or predictive model serving. (which could be beneficial for us when we are working with our ML models)
- **Developer-Friendly:** As someone relatively new to API development, I appreciate FastAPI's simplicity and its ability to automatically generate API documentation based on Python type hints. This feature not only saves time but also improves code readability and maintainability along with the fact that I don't need a lot of time to learn it as it is fairly easy and straight-forward.
- **Data Validation:** Using Pydantic, FastAPI ensures robust data validation, helping to catch errors early in the development process. This is especially important when handling diverse data inputs in machine learning applications and one of the most important reason I chose FastAPI and think that I will stick with it for future projects too.
- **Ecosystem Integration:** FastAPI seamlessly integrates with other Python libraries and frameworks, allowing me to extend its functionality with database integration, authentication mechanisms, and more, without complicating the core API logic. For example, I saw a lot of people using `SQLAcademy` online with FastAPI relatively easily along with other plotting libraries. As someone who works with Python extinsively, this makes my work even more easy and manageable rather than depending on cross-platform libraries for getting the things done.

### Why FastAPI Stands Out For Machine Learning
FastAPI’s strengths make it particularly suitable for building APIs around machine learning models:
- **Efficiency:** Its async design enables efficient handling of multiple requests concurrently, which is crucial for high-performance machine learning applications.

- **Data Safety:** With Pydantic’s strong data validation capabilities, FastAPI ensures that the data fed into machine learning models meets expected formats and types, reducing the risk of runtime errors.

- **Scalability:** FastAPI’s performance-oriented architecture and async capabilities support scalability, making it well-suited for applications that may experience increasing traffic or computational demands over time.

In summary, my exploration of FastAPI today has highlighted its potential to streamline API development, particularly for machine learning tasks where speed, data validation, and scalability are paramount. In the following sections, I look forward to diving deeper into implementing CRUD operations and integrating machine learning models effectively using FastAPI along with the code snippets I used for learning it.

## Seting up FastAPI
After looking around at some YouTube videos and getting a rough idea of what to do, the first thing I did was to try it out for myself.

### Getting Started with FastAPI
- Setting up FastAPI is surprisingly straightforward. All one needs is Pip to install FastAPI and Unicorn, an ASGI server needed to run FastAPI applications.
```bash
pip install fastapi uvicorn
```
- One can also install fastapi with all its dependencies like this:
```bash
pip install fastapi[all]
```

### Creating First Hello World FastAPI Project
With FastAPI installed, I created a new directory for my project and created a sample `main.py` file in it. This could be anything and I'm just naming it `main.py` for ease.

```python main.py
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def base():
    return 'Hello World!'
```

That's it. That's all it takes to run a simple FastAPI endpoint which could handle HTTP GET requests. I'll break it down for easier understanding:
- Import FastAPI and initalize an instance with it. I used `app` but one can use anything of their choice.
- Focus on `@app.get('/')`. This decorator tells Python to define a route for handling GET requests to the root URL `\` of my API. Here, `get` means that it is a `GET` request. In the brackets, we supply the url as well, in this case, it being `/` or the root. Thus, our API will look something like `localhost:8008/`
- After telling Python about the type of request (get in this case), I also made a function which is executed when a GET request is made to `/`. It returns a simple `Hello World` respone. Again, one can name the function anything rather than using `base`

### Running My FastAPI Application
To run the app locally, I used `Uvicorn` (which we installed earlier along with FastAPI). It is used to serve FastAPI applications.

```bash
uvicorn main:app --reload
```

- Here, `main` is the name of the module (Python file), whereas `app` is the name of the instance of FastAPI which we initialized in the file and will be using all throughout. 
- `--reload` simply means to enable automatic reloading of the server when changes are made to the code.

After running this, FastAPI started on `http://localhost:8000` by default. Navigating to this URL in my web browser displayed the JSON response: `{"Hello": "World"}`, confirming that my FastAPI application was up and running successfully.

### FastAPI's Interactive Documentation
One of the standout features of FastAPI is its automatic API documentation generation as it comes equipped with something known as `Swagger`. By navigating to `http://localhost:8000/docs` in my browser, I accessed the interactive Swagger UI documentation. This interface not only described my API endpoints but also allowed me to interact with them directly, testing different requests and seeing the responses in real-time.

## Exploring More Endpoints With FastAPI
After implementing a very simple and straightforward endpoint to test FastAPI's capabilities and lay the groundwork for more complex functionality, I started experimenting with other endpoints like POST, etc as well.

### Add Parameter to Endpoints
FastAPI makes it easy to handle parameters in API endpoints. For instance, I can modify the `base()` function to accept a `name` parameter and include it in the response:

```python
@app.get('/')
def base(name: str = "World"):
    return f'Hello {name}'
```

In this updated version:
- The `name` parameter is specified as a query parameter (?name=...) with a default value of "World". Also note that it only accepts `str` and giving it anything else, like an int, for example will throw up an error (exactly what we talked about earlier as how FastAPI handles data validation seemlessly and without any complicated stuff)
- Now, when accessing http://localhost:8000/?name=John, the response will be `"Hello John"`.
- This can further be extended with different functionalities but this is just a simple example on how to enforce data type validation and accepting parameters in our FastAPI GET requests.

### Handling POST Requests
To handle HTTP POST requests and accept data, I defined a new endpoint using the `@app.post()` decorator. This is a simple example from FastAPI's amazing documentation itself.

```python main.py
from pydantic import BaseModel

class Item(BaseModel):
    name : str
    descritpion: str = None
    price: float
    tax: float = None


@app.post('items/')
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        return f'Price with tax: {item.price} + {item.tax}'
```

- Here, Item is a `Pydantic` model that defines the structure of the data expected in the POST request body. It also helps keeping a check on the type of data which interacts with the API like enforcing data types (eg, `str` for name and descritpion, `float` for price and tax). Also, note how tax and description are not required arguments and have a default value of `None` just in case nothing is supplied for that.
- The `create_item()` function takes an `item` parameter of `type Item` and returns a dictionary representation of the item, returning the `price_with_tax` if tax is provided.

### Testing the Endpoint
To test the newly created POST endpoint, one can use tools like `Swagger` or `Postman`. I preferred to use `curl` as this is a very simple endpoint.

```bash
curl -X POST "http://localhost:8000/items/" -H "Content-Type: application/json" -d '{"name": "Example Item", "description": "An example item", "price": 50.0}'
```

- This sends a POST request to `http://localhost:8000/items/` with JSON data representing an item.

## CRUD Operations with FastAPI
After exploring some simple get and post requests, I went on to leverage FastAPI's capabilities to create endpoints for managing data, laying the groundwork for building robust APIs for ML applications later.

### Creating Data Models
To begin, I defined Pydantic models to represent the data structure that my API endpoints will handle. Here’s an example of defining a `User` model:

```python
from pydantic import BaseModel

class User(BaseModel):
    id : int
    username : str
    email : str
    full_name : str
```

- The `User` model specifies fields such as `id`, `username`, `email` and `full name`, ensuring type safety and data validation.

### Implementing CRUD endpoints
Using FastAPI's decorators `(@app.get, @app.post, @app.put, @app.delete)`, I implemented CRUD endpoints to perform operations on `User` data:

- **Create (POST):** Adding a new user to the database
```python
from typing import List

users = [] # for a simple demonstration

@app.post('/users/', response_model=User)
def create_user(user: User):
    users.append(user)
    return user
```

- **Read (GET):** Retreiving a list of all users or a specific user by ID.
```python
@app.get('/users/', response_model = List[User])
def read_users():
    return users

@app.get('/users/{user_id}', response_model = User)
def read_user(user_id : int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail = "User not found")
```

- **Update (PUT):** Updating an existing user's information
```python
@app.put('/users/{user_id}', response_model = User)
def update_user(user_id : int, updated_user : User):
    for user in users:
        if user.id == user_id:
            user.username = updated_user.username
            user.email = updated_user.email
            user.full_name = updated_user.full_name
            return user
    raise HTTPException(status_code = 404, detail = "User not found")
```

- **Delete (DELETE):** Deleting a user from the database
```python
@app.delete('/users/{user_id}', response_model = User)
def delete_user(user_id : int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    raise HTTPException(status_code = 404, detail = 'User not found')
```

### Testing CRUD Operations
To test the CRUD operations, I used `curl` as before:
- **Create (POST):** Send a POST request with JSON data representing a new user.
```bash
curl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d '{"id": 1, "username": "john_doe", "email": "john.doe@example.com", "full_name": "John Doe"}'
```

- **Read (GET):** Retrieve all users or a specific user by ID.
```bash
curl -X GET "http://localhost:8000/users/"
curl -X GET "http://localhost:8000/users/1"
```
- **Update (PUT):** Send a PUT request to update an existing user.
```bash
curl -X PUT "http://localhost:8000/users/1" -H "Content-Type: application/json" -d '{"username": "johndoe", "email": "johndoe@example.com", "full_name": "John Doe"}'
```

- **Delete (DELETE):** Send a DELETE request to remove a user by ID
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

## Integration with Machine Learning Models
Uptil this point, I was just messing around and getting my hands dirty with FastAPI and how to use it. Now, equipped with the knowledge of how to create atleast basic endpoints, I decided to give it a try with a pretrained model from PyTorch Zoo and implemented endpoints to make predictions using that.

### Loading a Pre-trained Machine Learning Model
First, I loaded a pre-trained `ResNet50` model from PyTorch zoo into my FastAPI app.
```python
import torch
from torchvision import models, transforms
from PIL import Image
from io import BytesIO
import requests
import numpy as np

# Load pretrained model
model = models.resnet50(pretrained = True)
model.eval()

# Define image transforms
transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
])
```

### Creating Prediction Endpoints
Next, I defined an endpoint in FastAPI `('/predict/')` to handle image classification predictions using the loaded ResNet50 model.

```python
from fastapi import FastAPI, File, UploadFile
from typing import List
import numpy as np

app = FastAPI()

@app.post('/predict')
def predict_image(file: UploadFile = File(...)):
    # Process the uploaded file
    img = Image.open(BytesIO(file.file.read()))
    img = transform(img) # apply transforms
    img = img.unsqueeze(0) # add batch dimension

    # Make predictions
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs, 1)
        predicted_class = predicted.item()

    return {'predicted_class' : predicted_class}
```
- **Explanation:** In this example, `predict_image()` accepts an uploaded image file `(file: UploadFile)`, processes it using the defined transformation `(transform)`, and then feeds it into the `ResNet50 model (model)`. After making a prediction, it returns the predicted class index `(predicted_class)`.

### Testing the Prediction Endpoint
To test the prediction endpoint, use the provided image file `(cat.png)` or any other image file you prefer. Here’s how you might test it using curl:

```bash
curl -X POST "http://localhost:8000/predict/" -H "Content-Type: multipart/form-data" -F "file=@cat.png"
```

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

> Photo by [Pawel Czerwinski](https://unsplash.com/@pawel_czerwinski) on [Unsplash](https://unsplash.com/)