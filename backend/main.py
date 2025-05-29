from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from models.generator import load_generator_and_generate
import uuid
import os
import traceback

app = FastAPI()

@app.post("/generate")
async def generate_image(request: Request):
    try:
        data = await request.json()
        z_dim = data.get("z", 100)

        os.makedirs("backend/static/generated", exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join("backend", "static", "generated", filename)

        load_generator_and_generate(z_dim=z_dim, save_path=output_path)

        return {"image_path": f"/static/generated/{filename}"}
    
    except Exception as e:
        traceback.print_exc()  # 터미널에 에러 메시지 출력됨
        return JSONResponse(status_code=500, content={"error": str(e)})
