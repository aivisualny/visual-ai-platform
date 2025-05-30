from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models.generator import load_generator_and_generate
import uuid
import os
import traceback
import torch
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
generated_folder = os.path.join(static_path, "generated_images")
app.mount("/static", StaticFiles(directory=static_path), name="static")

def clear_generated_images_except_epoch(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    for filename in os.listdir(folder_path):
        if not filename.startswith("epoch_"):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

clear_generated_images_except_epoch(generated_folder)

async def remove_file_later(file_path, delay=600):
    await asyncio.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)

@app.post("/generate")
async def generate_image(request: Request):
    try:
        data = await request.json()
        noise = data.get("noise", None)

        os.makedirs(generated_folder, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join(generated_folder, filename)

        if noise:
            z_tensor = torch.tensor(noise, dtype=torch.float32).view(1, 100)
        else:
            z_tensor = None

        load_generator_and_generate(z_tensor=z_tensor, save_path=output_path)

        asyncio.create_task(remove_file_later(output_path))

        return {"image_path": f"/static/generated_images/{filename}"}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
