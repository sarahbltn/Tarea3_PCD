import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
import models
from database import engine, Sessionlocal

load_dotenv()
API_KEY = os.getenv("API_KEY")
app = FastAPI(title="Users API", version="1.0.0")
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = Sessionlocal()
        yield db
    finally:
        db.close()
              
api_key_header = APIKeyHeader(name="User-API-KEY", description="API key por header", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Could not validate credentials")

class User(BaseModel):
    user_name: str = Field(...,min_length=1)
    user_email: EmailStr
    age: int | None = Field(default=None, ge=1, le=999)
    recommendations: list[str] = Field(default_factory=list) 
    ZIP : str | None = Field(default=None, min_length=5, max_length=9)

@app.get("/")
def root():
    return {"message": "user api up. see /Docs"}

@app.post("/api/v1/users/", tags=["User"])
def create_user(user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    existing_email = db.query(models.Users).filter(models.Users.user_email == user.user_email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="A user with that email already exists")
    
    user_model = models.Users(
        user_name = user.user_name,
        user_email = user.user_email,
        age = user.age,
        recommendations = user.recommendations,
        ZIP = user.ZIP
    )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.put("/api/v1/users/{user_id}", tags=["User"])
def update_user(user_id: int, user: User, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id ==  user_id).first()
    
    if user_model is None:
        raise HTTPException(status_code=404, detail=f"ID {user_id}: does not exist")
    user_model.user_name = user.user_name
    user_model.user_email = user.user_email
    user_model.age = user.age
    user_model.recommendations = user.recommendations
    user_model.ZIP = user.ZIP
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@app.get("/api/v1/users/{user_id}", tags=["User"])
def search_user(user_id:int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=400, detail=f"User with ID: {user_id} not found")
    return user_model

@app.delete("/api/v1/users/{user_id}", tags=["User"])
def delete_user(user_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    user_model = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=400, detail=f"User with ID: {user_id} not found")
    db.query(models.Users).filter(models.Users.user_id == user_id).delete()
    db.commit()
    return {"Deleted_users_id": user_id}
