import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from dataset import AgriculturalDataset, get_transforms
from model import PlantDiseaseModel
import time
import os

def train_engine():
    # Configuration
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    BATCH_SIZE = 32 # Optimized for RTX 4050 6GB VRAM
    LR = 3e-4
    EPOCHS = 20
    DATA_DIR = "./data/train" # Placeholder path
    
    print(f"🔥 Krishi-Chetan AI Engine Initialized")
    print(f"⚙️ Target Device: {DEVICE}")
    print(f"📂 Data Source: PlantVillage + PlantDoc Merged")

    # 1. Dataset & Loaders
    train_ds = AgriculturalDataset(DATA_DIR, mode='train', transform=get_transforms('train'))
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=4)
    
    # 2. Model
    model = PlantDiseaseModel(num_classes=38).to(DEVICE)
    
    # 3. Optimizer & Loss
    optimizer = optim.AdamW(model.parameters(), lr=LR)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1) # Label smoothing helps with noisy labels
    
    # 4. Training Loop
    scaler = torch.cuda.amp.GradScaler() # Mixed Precision for Speed on RTX 4050
    
    for epoch in range(EPOCHS):
        model.train()
        epoch_loss = 0
        
        # Simulate loop if no data present
        if len(train_ds) == 0:
            print("[INFO] No data found in ./data. Skipping actual training loop.")
            break
            
        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            
            optimizer.zero_grad()
            
            with torch.cuda.amp.autocast():
                outputs = model(images)
                loss = criterion(outputs, labels)
                
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            epoch_loss += loss.item()
            
        print(f"Epoch [{epoch+1}/{EPOCHS}] Loss: {epoch_loss:.4f}")
        
    # 5. Save Artifacts for Layout
    os.makedirs("weights", exist_ok=True)
    save_path = "weights/efficientnet_b4_krishi_chetan_v1.pth"
    torch.save(model.state_dict(), save_path)
    print(f"✅ Model saved to {save_path}")
    
    # Trigger Quantization export
    model.save_quantized("weights/efficientnet_b4_int8.pth")

if __name__ == "__main__":
    train_engine()
