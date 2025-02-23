from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.utils import create_access_token, verify_password
import jwt
from fastapi.security import HTTPBearer
from fastapi import Security, Depends
from app.utils import SECRET_KEY, ALGORITHM,hash_password
import datetime
from jose import jwt, JWTError

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    print("Getting DB")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
def register(id:str, username: str, password: str, role: str = "collaborator", db: Session = Depends(get_db)):
    """Register a new user."""
    print("Registering - ", id, username, password, role)
    user = db.query(User).filter(User.id == id).first()
    if user:
        raise HTTPException(status_code=400, detail="User ID already exists")
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user = User(id=id,username=username, password_hash=hash_password(password), role=role)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}



security = HTTPBearer()
def get_current_user(token: str = Security(security)):
    token = token.credentials  # ✅ Fix: Extract the token correctly

    print("✅ DEBUG: Extracted Token:", token)  # ✅ Print o
    if not token:
        # print("🚨 DEBUG: No Token Received")
        raise HTTPException(status_code=401, detail="No token provided")
    """Extracts user details from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("✅ DEBUG: Decoded Payload:", payload)
        return payload  # Contains username & role
    except JWTError as e:
        # print("🚨 DEBUG: JWT Error -->", e)  # ✅ Print error
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/user-profile")
def user_profile(user=Depends(get_current_user)):
    return {"username": user["sub"], "role": user["role"]}

@router.get("/me")
def get_user_details(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve the currently logged-in user details"""
    print("here")
    user = db.query(User).filter(User.username == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role
    }


def require_role(required_role: str):
    """Middleware to check if the user has the required role."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Permission denied")
        return current_user
    return role_checker