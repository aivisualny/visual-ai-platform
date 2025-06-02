import torch
from torchvision.utils import save_image
from .gan import Generator
import os
import uuid

def generate_gan_image(noise=None, z_dim=100):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Generator(z_dim=z_dim).to(device)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    checkpoint_path = os.path.join(base_dir, "checkpoints", "generator.pth")
    model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    model.eval()

    if noise is None:
        z_tensor = torch.randn(1, z_dim, device=device)
    else:
        z_tensor = torch.tensor(noise, dtype=torch.float32).view(1, z_dim).to(device)

    with torch.no_grad():
        fake_image = model(z_tensor).view(1, 1, 28, 28).cpu()

    static_dir = os.path.join(base_dir, "..", "static", "generated_images")
    os.makedirs(static_dir, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"
    save_path = os.path.join(static_dir, filename)
    save_image(fake_image, save_path, normalize=True)

    return f"/static/generated_images/{filename}"
