from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from app.services.auth_service import verify_token 
from PIL import Image
from io import BytesIO

router = APIRouter()

class RGBResponse(BaseModel):
    r: int
    g: int
    b: int

@router.post("/get_color", response_model=RGBResponse, status_code=200)
async def get_color(
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    try:
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert("RGB")
        r, g, b = image.getpixel((0, 0))
        
        return {"r": r, "g": g, "b": b}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al procesar la imagen: " + str(e))
