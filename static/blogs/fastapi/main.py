from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List

import torch
from torchvision import models, transforms
from PIL import Image
from io import BytesIO
import requests
import numpy as np

app = FastAPI()

## Section 2: Setting up FastAPI
# @app.get('/')
# def base():
#     return 'Hello World!'

## Section 3: Exploring More Endpoints with FastAPI
@app.get('/')
def base(name: str = "World"):
    return f'Hello {name}'

class Item(BaseModel):
    name : str
    descritpion: str = None
    price: float
    tax: float = None

@app.post('/items/')
def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        return f'Price with tax: {item.price + item.tax}'
    
### Section 4: CRUD operations with FastAPI
class User(BaseModel):
    id : int
    username : str
    email : str
    full_name : str

users = [] # for a simple demonstration

@app.post('/users/', response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@app.get('/users/', response_model = List[User])
def read_users():
    return users

@app.get('/users/{user_id}', response_model = User)
def read_user(user_id : int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail = "User not found")

@app.put('/users/{user_id}', response_model = User)
def update_user(user_id : int, updated_user : User):
    for user in users:
        if user.id == user_id:
            user.username = updated_user.username
            user.email = updated_user.email
            user.full_name = updated_user.full_name
            return user
    raise HTTPException(status_code = 404, detail = "User not found")

@app.delete('/users/{user_id}', response_model = User)
def delete_user(user_id : int):
    for index, user in enumerate(users):
        if user.id == user_id:
            deleted_user = users.pop(index)
            return deleted_user
    raise HTTPException(status_code = 404, detail = 'User not found')

## Section 5: Loading a Pre-Trained Machine Learning Model# Load pretrained model

# Load Pretrained model
model = models.resnet50(weights="ResNet50_Weights.DEFAULT")
model.eval()

# Define image transforms
transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
])

@app.post('/predict')
def predict_image(file: UploadFile = File(...)):
    # Process the uploaded file
    img = Image.open(BytesIO(file.file.read()))
    img = transforms(img) # apply transforms
    img = img.unsqueeze(0) # add batch dimension

    # Make predictions
    with torch.no_grad():
        outputs = model(img)
        _, predicted = torch.max(outputs, 1)
        predicted_class = predicted.item()

    return {'predicted_class' : predicted_class}



    
