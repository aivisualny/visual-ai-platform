import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import os

# 하이퍼파라미터
nz = 100
image_size = 64
batch_size = 128
num_epochs = 5
lr = 0.0002

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

transform = transforms.Compose([
    transforms.Resize(image_size),
    transforms.CenterCrop(image_size),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])
dataset = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            nn.ConvTranspose2d(nz, 256, 4, 1, 0, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 1, 4, 2, 1, bias=False),
            nn.Tanh()
        )

    def forward(self, input):
        return self.main(input)

class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            nn.Conv2d(1, 64, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(64, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Conv2d(128, 1, 4, 2, 1, bias=False),
            nn.Sigmoid()
        )

    def forward(self, input):
        out = self.main(input)
        return out.mean([1, 2, 3])

if __name__ == "__main__":
    netG = Generator().to(device)
    netD = Discriminator().to(device)
    criterion = nn.BCELoss()
    optimizerD = torch.optim.Adam(netD.parameters(), lr=lr, betas=(0.5, 0.999))
    optimizerG = torch.optim.Adam(netG.parameters(), lr=lr, betas=(0.5, 0.999))

    fixed_noise = torch.randn(64, nz, 1, 1, device=device)
    os.makedirs('backend/static/generated_images', exist_ok=True)
    os.makedirs('backend/models/checkpoints', exist_ok=True)

    for epoch in range(num_epochs):
        for i, (real, _) in enumerate(dataloader):
            real = real.to(device)
            b_size = real.size(0)
            noise = torch.randn(b_size, nz, 1, 1, device=device)
            fake = netG(noise)

            # Discriminator
            optimizerD.zero_grad()
            label_real = torch.full((b_size,), 1.0, device=device)
            output_real = netD(real)
            lossD_real = criterion(output_real, label_real)

            label_fake = torch.full((b_size,), 0.0, device=device)
            output_fake = netD(fake.detach())
            lossD_fake = criterion(output_fake, label_fake)

            lossD = lossD_real + lossD_fake
            lossD.backward()
            optimizerD.step()

            # Generator
            optimizerG.zero_grad()
            label_gen = torch.full((b_size,), 1.0, device=device)
            output_gen = netD(fake)
            lossG = criterion(output_gen, label_gen)
            lossG.backward()
            optimizerG.step()

        with torch.no_grad():
            fake = netG(fixed_noise).detach().cpu()
            grid = torchvision.utils.make_grid(fake, padding=2, normalize=True)
            plt.imshow(grid.permute(1, 2, 0).numpy())
            plt.axis("off")
            plt.savefig(f"backend/static/generated_images/epoch_{epoch+1}.png")
            plt.close()
            print(f"[✔] epoch_{epoch+1}.png 저장 완료")

    # 모델 저장
    torch.save(netG.state_dict(), "backend/models/checkpoints/generator.pth")
    print("훈련 완료 및 모델 저장 완료!")
