import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import os

# 하이퍼파라미터
z_dim = 100
img_size = 28
img_dim = img_size * img_size
batch_size = 128
num_epochs = 5
lr = 0.0002

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])
dataset = torchvision.datasets.MNIST(root='data', train=True, download=True, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

class Generator(nn.Module):
    def __init__(self, z_dim=100, img_dim=784):
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(z_dim, 256),
            nn.ReLU(True),
            nn.Linear(256, 512),
            nn.ReLU(True),
            nn.Linear(512, img_dim),
            nn.Tanh()
        )

    def forward(self, x):
        return self.main(x)

class Discriminator(nn.Module):
    def __init__(self, img_dim=784):
        super().__init__()
        self.disc = nn.Sequential(
            nn.Linear(img_dim, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.disc(x)

if __name__ == "__main__":
    netG = Generator(z_dim, img_dim).to(device)
    netD = Discriminator(img_dim).to(device)

    criterion = nn.BCELoss()
    optimizerD = torch.optim.Adam(netD.parameters(), lr=lr, betas=(0.5, 0.999))
    optimizerG = torch.optim.Adam(netG.parameters(), lr=lr, betas=(0.5, 0.999))

    fixed_noise = torch.randn(64, z_dim, device=device)
    os.makedirs('static/generated_images', exist_ok=True)
    os.makedirs('backend/models/checkpoints', exist_ok=True)

    for epoch in range(num_epochs):
        for real, _ in dataloader:
            real = real.view(-1, img_dim).to(device)
            b_size = real.size(0)
            noise = torch.randn(b_size, z_dim, device=device)
            fake = netG(noise)

            # Discriminator 훈련
            optimizerD.zero_grad()
            label_real = torch.ones(b_size, device=device)
            label_fake = torch.zeros(b_size, device=device)

            output_real = netD(real).view(-1)
            lossD_real = criterion(output_real, label_real)

            output_fake = netD(fake.detach()).view(-1)
            lossD_fake = criterion(output_fake, label_fake)

            lossD = lossD_real + lossD_fake
            lossD.backward()
            optimizerD.step()

            # Generator 훈련
            optimizerG.zero_grad()
            output_gen = netD(fake).view(-1)
            lossG = criterion(output_gen, label_real)
            lossG.backward()
            optimizerG.step()

        print(f"[✔] Epoch {epoch+1}/{num_epochs} 완료")

        with torch.no_grad():
            fake = netG(fixed_noise).view(-1, 1, img_size, img_size)
            torchvision.utils.save_image(
                fake, f"static/generated_images/epoch_{epoch+1}.png", normalize=True, nrow=8
            )

    torch.save(netG.state_dict(), "backend/models/checkpoints/generator.pth")
    print("훈련 완료 및 모델 저장 완료!")
