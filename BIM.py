import os
from typing import Optional, List
from contextlib import asynccontextmanager
from pathlib import Path




import faker
# Data base and models.
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List

#Servers and Api
from fastapi import FastAPI, HTTPException, status

#Gemini

from google import genai

# User Interface (Frontend)
import streamlit as st
import requests #To connect streamlit with FastAPI

# Config for environmental variables
from dotenv import load_dotenv

from urllib.parse import quote_plus

#load the variables
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

#Data base credentials and API
GENAI_KEY = os.getenv("Genai_key")
DB_HOST = os.getenv("MySQL_HOST") or "localhost"

#Added this extra to clean the port in order to avoid empty chains
raw_port = os.getenv("MySQL_PORT")
DB_PORT = raw_port.strip() if raw_port and raw_port.strip() else "3306"

DB_USER = os.getenv("MySQL_USER") or "root"
DB_PASS = os.getenv("MySQL_PASS") or ""
DB_NAME = os.getenv("MySQL_DATABASE")

#If the password has especial characters this line is needed
safe_password = quote_plus(DB_PASS)

#Connection Chain
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#Create engine connection
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

#Model base for inventory data
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float
    quantity: int = 0


#Life Cycle management
@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="BIM-MAnagement",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/product/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


@app.get("/products/", response_model=list[Product])
def get_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products