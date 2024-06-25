import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Token
from auth import login_user, register_user
import models
from database import engine
import uvicorn

logger = logging.getLogger("uvicorn")

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

environment = "dev"
if environment == "dev":
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get('/')
def index():
    return {"message": "Hello world!"}

@app.post("/login", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends()) -> Token:
  access_token = await login_user(user)
  return access_token

@app.post("/register", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends()) -> Token:
  access_token = await register_user(user)
  return access_token

@app.post("/token", response_model=Token)
async def login(user: OAuth2PasswordRequestForm = Depends()) -> Token:
  access_token = await login_user(user)
  return access_token

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
