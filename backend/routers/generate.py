from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.generator import generate_gan_image
from models.diffusion import generate_diffusion_image

router = APIRouter()

@router.post("/generate/gan")
async def generate_gan(request: Request):
    try:
        data = await request.json()
        noise = data.get("noise")
        image_path = generate_gan_image(noise)
        return JSONResponse(content={"image_path": image_path})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@router.post("/generate/diffusion")
async def generate_diffusion():
    try:
        image_path = generate_diffusion_image()
        return JSONResponse(content={"image_path": image_path})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
