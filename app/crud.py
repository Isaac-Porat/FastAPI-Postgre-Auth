import logging
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import engine
from auth import get_password_hash
from sqlalchemy.orm import Session
from models import UserModel

logger = logging.getLogger("uvicorn")

async def fetch_all_user():
    try:
        with Session(engine) as session:
            users = session.query(UserModel).all()
            return users

    except Exception as e:
        logger.error(f"Unexpected error while fetching all users: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while fetching all users.",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def delete_all_users():
    try:
        with Session(engine) as session:
            deleted_count = session.query(UserModel).filter(UserModel.is_admin != True).delete()
            session.commit()

            if deleted_count == 0:
                return {"message": "No users to delete"}
    except Exception as e:
        logger.error(f"Unexpected error while deleting all users: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while deleting all users.",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def fetch_user(username: str):
    try:
        with Session(engine) as session:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            if user:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No user found."
                )

    except Exception as e:
        logger.error(f"Unexpected error while fetching user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while fetching user.",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def delete_user(username: str):
    try:
        with Session(engine) as session:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            if user:
                session.delete(user)
                session.commit()
                return {"message": "User deleted successfully"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )
    except Exception as e:
        logger.error(f"Unexpected error while deleting user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while deleting user.",
            headers={"WWW-Authenticate": "Bearer"}
        )

async def create_new_user(user_data: OAuth2PasswordRequestForm = Depends()):
    try:
        with Session(engine) as session:

            if session.query(UserModel).filter(UserModel.username == user_data.username).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists"
                )

            hashed_password = get_password_hash(user_data.password)

            user = UserModel(username=user_data.username, password=hashed_password)
            session.add(user)
            session.commit()

            return {"status": "success", "message": "New user created successfully"}, 200

    except Exception as e:
        logger.error(f"Unexpected error while creating a new user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error while creating a new user.",
            headers={"WWW-Authenticate": "Bearer"}
        )