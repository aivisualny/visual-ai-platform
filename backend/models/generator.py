import torch
from torchvision.utils import save_image
from .dcgan_train import Generator
import os

def load_generator_and_generate(z_dim=100, save_path="generated.png"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model = Generator().to(device)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    pth_path = os.path.join(base_dir, "checkpoints", "generator.pth")
    
    model.load_state_dict(torch.load(pth_path, map_location=device))
    model.eval()

    noise = torch.randn(1, z_dim, 1, 1, device=device)
    with torch.no_grad():
        fake_image = model(noise).detach().cpu()
    save_image(fake_image, save_path, normalize=True)
