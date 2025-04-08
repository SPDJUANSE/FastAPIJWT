# app/routes/auth_routes.py
from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

JWT_EXPIRATION_MINUTES = int(os.environ.get("JWT_EXPIRATION_MINUTES", 30))

@router.post("/register", response_model=Token)
async def register(user: UserRegister, db: AsyncIOMotorDatabase = Depends(get_database)):
    if await db.users.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    

    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "nombre": user.nombre,
        "password": hashed_password
    }
    result = await db.users.insert_one(user_data)
    
 
    token = create_access_token(
        {"sub": str(result.inserted_id)},
        expires_delta=timedelta(minutes=JWT_EXPIRATION_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncIOMotorDatabase = Depends(get_database)):

    db_user = await db.users.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token(
        {"sub": str(db_user["_id"])},
        expires_delta=timedelta(minutes=JWT_EXPIRATION_MINUTES)
    )
    return {"access_token": token, "token_type": "bearer"}
