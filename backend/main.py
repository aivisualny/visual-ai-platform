from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models.generator import load_generator_and_generate
import uuid
import os
import traceback
import torch

app = FastAPI()

# CORS 설정: 프론트엔드와 통신 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev 서버 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 이미지 저장 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.post("/generate")
async def generate_image(request: Request):
    try:
        data = await request.json()
        noise = data.get("noise", None)  # 노이즈 벡터 수신

        os.makedirs("static/generated_images", exist_ok=True)
        filename = f"{uuid.uuid4().hex}.png"
        output_path = os.path.join("static", "generated_images", filename)

        if noise:
            # 리스트를 torch tensor로 변환
            z_tensor = torch.tensor(noise, dtype=torch.float32).view(1, 100, 1, 1)
        else:
            z_tensor = None  # 무작위 노이즈 생성

        # 생성자 모델로 이미지 생성
        load_generator_and_generate(z_tensor=z_tensor, save_path=output_path)

        return {"image_path": f"/static/generated_images/{filename}"}

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
