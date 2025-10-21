from fastapi import FastAPI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import uvicorn
import os

load_dotenv()
app = FastAPI(title="Simple FastAPI App", version="1.0.0")
data=[{"name": "Sam Larry", "age": 20, "track": "AI Developer"},
      {"name": "Bahuballi", "age": 20, "track": "Backend Developer"},
      {"name": "John Doe", "age": 20, "track": "Frontend Developer"}]

class Item(BaseModel):
    name: str = Field(..., example="Perpetual")
    age: int = Field(..., example=25)
    track: str = Field(..., example="Fullstack Developer")

@app.get("/", description= "This endpoint just returns a welcome message")
def root():
    return { "Message": "Welcome to my FastAPI Application"}

@app.get("/get-data")
def get_data():
    return data

@app.post("/create-data")
def create_data(req: Item):
    data.append(req.dict())
    return{"Message": "Data Received", "Data": data}

@app.put("/update-data/{id}")
def update_data(id:int, req:Item):
    data[id] = req.dict()
    # print(data)
    return{"message": "Data updated", "Data":data}

@app.delete("/delete-data/{id}")
def delete_data(id: int):
    if id < 0 or id >= len(data):
        return {"error": "Invalid ID"}
    deleted_item = data.pop(id)
    # print(data)
    return {"message": "Data deleted", "Deleted Item": deleted_item, "Data": data}


@app.patch("/update-partial/{id}")
def update_partial(id: int, req: Item):
    if id < 0 or id >= len(data):
        return {"error": "Invalid ID"}
    
    existing_item = data[id]
    
    updates = req.dict(exclude_unset=True)  
    for key, value in updates.items():
        existing_item[key] = value
    
    data[id] = existing_item
    # print(data)
    return {"message": "Data partially updated", "Updated Data": existing_item}
