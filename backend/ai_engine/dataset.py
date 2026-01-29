import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as transforms

class AgriculturalDataset(Dataset):
    """
    Hybrid Dataset Loader for PlantVillage (Global) and PlantDoc (Indian Context).
    
    Strategy:
    - We merge PlantVillage for 'Baseline Features' (Symptoms).
    - We merge PlantDoc for 'Environmental Robustness' (Lighting, Soil Background).
    """
    def __init__(self, root_dir, mode='train', transform=None):
        self.root_dir = root_dir
        self.mode = mode
        self.transform = transform
        self.image_paths = []
        self.labels = []
        
        # Walk through the directory structure: root/class_name/image.jpg
        # Expected structure:
        # data/
        #   train/
        #     Apple___Black_rot/
        #     Corn___Common_rust/
        #     ...
        
        if os.path.exists(root_dir):
            self.classes = sorted(os.listdir(root_dir))
            for label_idx, class_name in enumerate(self.classes):
                class_dir = os.path.join(root_dir, class_name)
                if os.path.isdir(class_dir):
                    for img_name in os.listdir(class_dir):
                        self.image_paths.append(os.path.join(class_dir, img_name))
                        self.labels.append(label_idx)
        else:
            print(f"[WARN] Dataset path {root_dir} not found. Ensure data is downloaded.")

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_transforms(mode='train'):
    """
    Returns production-grade augmentations.
    We use strong ColorJitter to handle 'Evening/Morning' lighting conditions in villages.
    """
    if mode == 'train':
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            # Key for outdoor robustness:
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
