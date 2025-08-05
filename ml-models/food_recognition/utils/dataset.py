"""
Dataset classes for food image recognition
"""

import os
import json
import torch
import numpy as np
from PIL import Image
from pathlib import Path
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import albumentations as A
from albumentations.pytorch import ToTensorV2

class FoodDataset(Dataset):
    """Dataset class for food image recognition"""
    
    def __init__(self, data_dir, split='train', transform=None, class_mapping=None):
        """
        Args:
            data_dir (str): Path to the organized dataset directory
            split (str): Dataset split ('train', 'val', 'test')
            transform: Image transformations
            class_mapping (dict): Mapping from class names to indices
        """
        self.data_dir = Path(data_dir)
        self.split = split
        self.transform = transform
        
        # Load class mapping
        if class_mapping is None:
            class_mapping_file = self.data_dir.parent / "class_mapping.json"
            if class_mapping_file.exists():
                with open(class_mapping_file, 'r') as f:
                    self.class_mapping = json.load(f)
            else:
                # Create class mapping from directory structure
                split_dir = self.data_dir / split
                classes = sorted([d.name for d in split_dir.iterdir() if d.is_dir()])
                self.class_mapping = {class_name: idx for idx, class_name in enumerate(classes)}
        else:
            self.class_mapping = class_mapping
        
        # Create reverse mapping
        self.idx_to_class = {idx: class_name for class_name, idx in self.class_mapping.items()}
        
        # Load image paths and labels
        self.images = []
        self.labels = []
        
        split_dir = self.data_dir / split
        for class_name, class_idx in self.class_mapping.items():
            class_dir = split_dir / class_name
            if class_dir.exists():
                for img_path in class_dir.glob("*.jpg"):
                    self.images.append(str(img_path))
                    self.labels.append(class_idx)
        
        print(f"Loaded {len(self.images)} images for {split} split")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        # Load image
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')
        
        # Get label
        label = self.labels[idx]
        
        # Apply transformations
        if self.transform:
            image = self.transform(image)
        
        return image, label
    
    def get_class_names(self):
        """Get list of class names"""
        return [self.idx_to_class[i] for i in range(len(self.idx_to_class))]

def get_transforms(image_size=224, split='train'):
    """Get image transformations for different splits"""
    
    if split == 'train':
        # Training transforms with augmentation
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        # Validation/Test transforms (no augmentation)
        transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    
    return transform

def get_albumentations_transforms(image_size=224, split='train'):
    """Get Albumentations transforms for better augmentation"""
    
    if split == 'train':
        transform = A.Compose([
            A.Resize(image_size, image_size),
            A.HorizontalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.RandomBrightnessContrast(p=0.2),
            A.HueSaturationValue(p=0.2),
            A.OneOf([
                A.MotionBlur(p=0.2),
                A.MedianBlur(blur_limit=3, p=0.1),
                A.Blur(blur_limit=3, p=0.1),
            ], p=0.2),
            A.OneOf([
                A.OpticalDistortion(p=0.3),
                A.GridDistortion(p=0.1),
                A.IAAPiecewiseAffine(p=0.3),
            ], p=0.2),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
    else:
        transform = A.Compose([
            A.Resize(image_size, image_size),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
    
    return transform

class AlbumentationsDataset(Dataset):
    """Dataset class using Albumentations for better augmentation"""
    
    def __init__(self, data_dir, split='train', transform=None, class_mapping=None):
        self.data_dir = Path(data_dir)
        self.split = split
        self.transform = transform
        
        # Load class mapping
        if class_mapping is None:
            class_mapping_file = self.data_dir.parent / "class_mapping.json"
            if class_mapping_file.exists():
                with open(class_mapping_file, 'r') as f:
                    self.class_mapping = json.load(f)
            else:
                split_dir = self.data_dir / split
                classes = sorted([d.name for d in split_dir.iterdir() if d.is_dir()])
                self.class_mapping = {class_name: idx for idx, class_name in enumerate(classes)}
        else:
            self.class_mapping = class_mapping
        
        self.idx_to_class = {idx: class_name for class_name, idx in self.class_mapping.items()}
        
        # Load image paths and labels
        self.images = []
        self.labels = []
        
        split_dir = self.data_dir / split
        for class_name, class_idx in self.class_mapping.items():
            class_dir = split_dir / class_name
            if class_dir.exists():
                for img_path in class_dir.glob("*.jpg"):
                    self.images.append(str(img_path))
                    self.labels.append(class_idx)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        # Load image
        img_path = self.images[idx]
        image = np.array(Image.open(img_path).convert('RGB'))
        
        # Get label
        label = self.labels[idx]
        
        # Apply transformations
        if self.transform:
            transformed = self.transform(image=image)
            image = transformed['image']
        
        return image, label
    
    def get_class_names(self):
        return [self.idx_to_class[i] for i in range(len(self.idx_to_class))]

def create_data_loaders(data_dir, batch_size=32, num_workers=4, image_size=224, use_albumentations=True):
    """Create data loaders for train, validation, and test sets"""
    
    if use_albumentations:
        # Use Albumentations transforms
        train_transform = get_albumentations_transforms(image_size, 'train')
        val_transform = get_albumentations_transforms(image_size, 'val')
        test_transform = get_albumentations_transforms(image_size, 'test')
        
        # Create datasets
        train_dataset = AlbumentationsDataset(data_dir, 'train', train_transform)
        val_dataset = AlbumentationsDataset(data_dir, 'val', val_transform)
        test_dataset = AlbumentationsDataset(data_dir, 'test', test_transform)
    else:
        # Use torchvision transforms
        train_transform = get_transforms(image_size, 'train')
        val_transform = get_transforms(image_size, 'val')
        test_transform = get_transforms(image_size, 'test')
        
        # Create datasets
        train_dataset = FoodDataset(data_dir, 'train', train_transform)
        val_dataset = FoodDataset(data_dir, 'val', val_transform)
        test_dataset = FoodDataset(data_dir, 'test', test_transform)
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset, 
        batch_size=batch_size, 
        shuffle=True, 
        num_workers=num_workers,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset, 
        batch_size=batch_size, 
        shuffle=False, 
        num_workers=num_workers,
        pin_memory=True
    )
    
    return train_loader, val_loader, test_loader, train_dataset.class_mapping 