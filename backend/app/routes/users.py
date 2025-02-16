from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models import User
from app.schemas import UserCreate, UserResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils import create_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)