import os
import logging
from fastapi import Depends, HTTPException, status
from auth import get_current_user, get_password_hash
from database import engine
from models import UserModel
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("uvicorn")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

async def create_admin():
  try:
    with Session(engine) as session:
      if session.query(UserModel).filter(UserModel.username == ADMIN_USERNAME, UserModel.is_admin == True).first():
        return {"status": "success", "message": "Admin user already exists"}, 200

      admin_user = UserModel(username=ADMIN_USERNAME, password=get_password_hash(ADMIN_PASSWORD), is_admin=True)
      if admin_user:
        session.add(admin_user)
        session.commit()

        return {"status": "success", "message": "Admin user created successfully"}, 200
  except Exception as e:
    logger.error(f"Unexpected error while creating admin user: {e}", exc_info=True)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Unexpected error while creating admin user.",
      headers={"WWW-Authenticate": "Bearer"}
    )

async def get_current_admin_user(token: str = Depends(get_current_user)):
  adminUsername = token

  if adminUsername != ADMIN_USERNAME:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Unauthorized access attempt by non-admin user",
      headers={"WWW-Authenticate": "Bearer"},
    )

  try:
    with Session(engine) as session:
      admin_user = session.query(UserModel).filter(UserModel.username == adminUsername, UserModel.is_admin == True).first()
      if not admin_user:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Unauthorized access attempt by non-admin user",
          headers={"WWW-Authenticate": "Bearer"},
        )

      return adminUsername

  except Exception as e:
    logger.error(f"Unexpected error while creating admin user: {e}", exc_info=True)
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Unexpected error while creating admin user.",
      headers={"WWW-Authenticate": "Bearer"}
    )
