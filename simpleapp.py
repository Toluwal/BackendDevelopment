import database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="simple App", version="1.0.0")
