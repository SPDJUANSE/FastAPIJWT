# main.py
from fastapi import FastAPI
from app.routes.sitios_routes import router as sitio_router
from app.routes.auth_routes import router as auth_router
from app.routes.rgb_routes import router as rgb_router 
from app.db.database import connect_to_mongo, close_mongo_connection
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv() 

origins = [
    "http://localhost:5500",  
    "http://127.0.0.1:5500",
]




app = FastAPI(title="API de Sitios Turísticos en Bogotá")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(rgb_router, prefix="/rgb", tags=["RGB"])
app.include_router(sitio_router, prefix="/sitios", tags=["sitios"])
