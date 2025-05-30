import torch
from torchvision.utils import save_image
from .gan_train import Generator
import os

def load_generator_and_generate(z_tensor=None, z_dim=100, save_path=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = Generator(z_dim=z_dim).to(device)

    # MLP 구조에 맞는 새로 저장한 .pth 불러오기
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pth_path = os.path.join(base_dir, "checkpoints", "generator.pth")
    model.load_state_dict(torch.load(pth_path, map_location=device))
    model.eval()

    if z_tensor is None:
        z_tensor = torch.randn(1, z_dim, device=device)
    else:
        z_tensor = z_tensor.to(device)

    with torch.no_grad():
        fake_image = model(z_tensor).view(1, 1, 28, 28).detach().cpu()

    if save_path is None:
        static_dir = os.path.join(base_dir, "..", "static", "generated_images")
        os.makedirs(static_dir, exist_ok=True)
        save_path = os.path.join(static_dir, "generated.png")

    save_image(fake_image, save_path, normalize=True)
