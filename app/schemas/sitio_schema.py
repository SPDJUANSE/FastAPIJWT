# app/schemas/sitio_schema.py
from pydantic import BaseModel
from typing import Optional

class Sitio(BaseModel):
    _id: str = None
    nombre: str
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class SitioResponse(Sitio):
    id: str
