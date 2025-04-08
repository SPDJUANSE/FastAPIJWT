# app/db/database.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
client = None

async def connect_to_mongo():
    global client
    client = AsyncIOMotorClient(MONGO_URI)
    print("Conectado a MongoDB")

async def close_mongo_connection():
    global client
    client.close()
    print("Desconectado de MongoDB")

def get_database():
    if client is None:
        raise HTTPException(status_code=500, detail="No hay conexión a la base de datos")
    return client.turismo  # Nombre de la base de datos
