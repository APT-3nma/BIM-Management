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
import os
from dotenv import load_dotenv

