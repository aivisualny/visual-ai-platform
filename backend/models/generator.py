import torch
from torchvision.utils import save_image
from .dcgan_train import Generator
import os

def load_generator_and_generate(z_tensor=None, z_dim=100, save_path="generated.png"):
    # 디바이스 설정
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 생성자 모델 초기화 및 불러오기
    model = Generator().to(device)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pth_path = os.path.join(base_dir, "checkpoints", "generator.pth")
    model.load_state_dict(torch.load(pth_path, map_location=device))
    model.eval()

    # z_tensor가 있으면 그걸 사용하고, 없으면 무작위 노이즈 생성
    if z_tensor is None:
        z_tensor = torch.randn(1, z_dim, 1, 1, device=device)
    else:
        z_tensor = z_tensor.to(device)

    # 이미지 생성
    with torch.no_grad():
        fake_image = model(z_tensor).detach().cpu()

    # 이미지 저장
    save_image(fake_image, save_path, normalize=True)
