from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import Response
from typing import Optional
import jwt
from datetime import datetime, time, timedelta
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class Item(BaseModel):
    name : str = Field(..., decription = "The name of the item")
    price : float = Field(..., gt = 0, decription = "The price of the item")

@app.post('/items/')
def create_item(item: Item):
    return {'name' : item.name, 'price' : item.price}

@app.get('items/{item_id}')
def read_item(item_id : int):
    if item_id not in range(1, 6):
        raise HTTPException(status_code = 404, detail = "Item not found")
    return {'item' : item_id}

# Secret key to sign JWT tokens
SECRET_KEY = "mysecretkey"
# Token expiration time in minutes
TOKEN_EXPIRATION = 30

# Example user data (normally this would come from a database)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedpassword",
    }
}

# Pydantic models
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserInDB(User):
    hashed_password: str

# OAuth2 scheme using JWT tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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

## Section 3: Metrics
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


