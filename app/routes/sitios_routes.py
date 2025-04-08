
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.sitio_schema import Sitio, SitioResponse
from app.db.database import get_database
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.services.auth_service import verify_token

router = APIRouter()

def sitio_helper(sitio: dict) -> dict:
    return {
        "id": str(sitio["_id"]),
        "nombre": sitio["nombre"],
        "descripcion": sitio.get("descripcion"),
        "direccion": sitio.get("direccion"),
        "latitud": sitio.get("latitud"),
        "longitud": sitio.get("longitud")
    }

@router.get("/", response_model=list[SitioResponse])
async def get_sitios(db: AsyncIOMotorDatabase = Depends(get_database)):
    sitios = []
    async for sitio in db.sitios.find():
        sitios.append(sitio_helper(sitio))
    return sitios

@router.post("/", response_model=SitioResponse, status_code=201)
async def create_sitio(
    sitio: Sitio,
    db: AsyncIOMotorDatabase = Depends(get_database),
    token: str = Depends(verify_token)
):
    sitio_dict = sitio.dict()
    sitio_dict["_id"] = sitio_dict["nombre"]
    await db.sitios.insert_one(sitio_dict)
    nuevo_sitio = await db.sitios.find_one({"_id": sitio_dict["nombre"]})
    return sitio_helper(nuevo_sitio)

@router.get("/{id}", response_model=SitioResponse)
async def get_sitio(id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    sitio = await db.sitios.find_one({"_id": id})
    if sitio:
        return sitio_helper(sitio)
    raise HTTPException(status_code=404, detail="Sitio no encontrado")

@router.put("/{id}", response_model=SitioResponse)
async def update_sitio(
    id: str,
    sitio: Sitio,
    db: AsyncIOMotorDatabase = Depends(get_database),
    token: str = Depends(verify_token)
):
    sitio_data = {k: v for k, v in sitio.dict().items() if v is not None}
    result = await db.sitios.update_one({"_id": id}, {"$set": sitio_data})
    if result.modified_count:
        sitio_actualizado = await db.sitios.find_one({"_id": id})
        return sitio_helper(sitio_actualizado)
    raise HTTPException(status_code=404, detail="Sitio no encontrado")

@router.delete("/{id}")
async def delete_sitio(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
    token: str = Depends(verify_token)
):
    result = await db.sitios.delete_one({"_id": id})
    if result.deleted_count:
        return {"message": "Sitio eliminado"}
    raise HTTPException(status_code=404, detail="Sitio no encontrado")
