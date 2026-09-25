import os
from typing import Optional, List
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime
from enum import Enum




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

# Categories table
class Category(SQLModel, table=True):
    __tablename__ = "categories"
    category_id:Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None

# Suppliers table
class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"
    supplier_id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    contact_email: Optional[str] = None
    phone: Optional[str] = None

#Model base for inventory data
class InventoryItem(SQLModel, table=True):
    __tablename__ = "inventory"

    item_id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(unique=True, index=True)
    name: str = Field(index=True)
    category_id: Optional[int] = Field(default=None, foreign_key="categories.category_id")
    supplier_id: Optional[int] = Field(default=None, foreign_key="suppliers.supplier_id")
    stock_quantity: int = Field(default=0)
    unit_price: float
    location: Optional[str] = None

# Defining Transaction Type
class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"

#Transaction model
class InventioryTransaction(SQLModel, table=True):
    __tablename__ = "inventory_transactions"

    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    item_id: int = Field(foreign_key="inventory.item_id")
    transaction_type: TransactionType
    quantity: int
    trasaction_dat: datetime = Field(default_factory=datetime.utcnow)
    user_reference: Optional[str] = None



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

@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(item: InventoryItem):
    with Session(engine) as session:
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@app.get("/items/", response_model=list[InventoryItem])
def get_items():
    with Session(engine) as session:
        items = session.exec(select(InventoryItem)).all()
        return items