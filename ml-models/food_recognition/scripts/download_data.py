#!/usr/bin/env python3
"""
Download and prepare the Food-101 dataset for training
"""

import os
import requests
import zipfile
import tarfile
from pathlib import Path
from tqdm import tqdm
import shutil

def download_file(url, filename):
    """Download a file with progress bar"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            pbar.update(size)

def extract_archive(archive_path, extract_to):
    """Extract archive file"""
    print(f"Extracting {archive_path} to {extract_to}")
    
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith('.tar.gz'):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path}")

def setup_food101_dataset():
    """Download and setup Food-101 dataset"""
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Food-101 dataset URLs
    base_url = "https://data.vision.ee.ethz.ch/cvl/food-101.tar.gz"
    dataset_file = data_dir / "food-101.tar.gz"
    
    # Download dataset if not exists
    if not dataset_file.exists():
        print("Downloading Food-101 dataset...")
        download_file(base_url, dataset_file)
    else:
        print("Food-101 dataset already downloaded.")
    
    # Extract dataset
    if not (data_dir / "food-101").exists():
        print("Extracting Food-101 dataset...")
        extract_archive(dataset_file, data_dir)
    else:
        print("Food-101 dataset already extracted.")
    
    # Organize the dataset structure
    food101_dir = data_dir / "food-101"
    images_dir = food101_dir / "images"
    meta_dir = food101_dir / "meta"
    
    # Create organized structure
    organized_dir = data_dir / "organized"
    organized_dir.mkdir(exist_ok=True)
    
    # Create train/val/test directories
    for split in ['train', 'val', 'test']:
        (organized_dir / split).mkdir(exist_ok=True)
    
    # Read class names
    classes_file = meta_dir / "classes.txt"
    with open(classes_file, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    
    print(f"Found {len(classes)} food classes")
    
    # Create class directories and organize images
    for split in ['train', 'test']:
        split_file = meta_dir / f"{split}.txt"
        
        if split_file.exists():
            with open(split_file, 'r') as f:
                image_list = [line.strip() for line in f.readlines()]
            
            print(f"Processing {split} split with {len(image_list)} images...")
            
            for image_name in tqdm(image_list, desc=f"Organizing {split} images"):
                # Extract class name from image name (format: class_name/image_id.jpg)
                class_name = image_name.split('/')[0]
                
                # Create class directory
                class_dir = organized_dir / split / class_name
                class_dir.mkdir(exist_ok=True)
                
                # Copy image
                src_path = images_dir / f"{image_name}.jpg"
                dst_path = class_dir / f"{image_name.split('/')[1]}.jpg"
                
                if src_path.exists():
                    shutil.copy2(src_path, dst_path)
    
    # Create validation split from training data
    train_dir = organized_dir / "train"
    val_dir = organized_dir / "val"
    
    print("Creating validation split...")
    for class_name in classes:
        class_train_dir = train_dir / class_name
        class_val_dir = val_dir / class_name
        class_val_dir.mkdir(exist_ok=True)
        
        if class_train_dir.exists():
            images = list(class_train_dir.glob("*.jpg"))
            # Move 10% of images to validation
            num_val = max(1, len(images) // 10)
            
            for img in images[:num_val]:
                shutil.move(str(img), str(class_val_dir / img.name))
    
    print("Dataset organization complete!")
    print(f"Dataset location: {organized_dir}")
    
    # Print statistics
    for split in ['train', 'val', 'test']:
        split_dir = organized_dir / split
        total_images = sum(len(list((split_dir / class_name).glob("*.jpg"))) 
                          for class_name in classes 
                          if (split_dir / class_name).exists())
        print(f"{split.capitalize()}: {total_images} images")

def create_class_mapping():
    """Create a mapping from class names to indices"""
    data_dir = Path("data")
    organized_dir = data_dir / "organized"
    train_dir = organized_dir / "train"
    
    classes = sorted([d.name for d in train_dir.iterdir() if d.is_dir()])
    
    # Create class to index mapping
    class_to_idx = {class_name: idx for idx, class_name in enumerate(classes)}
    
    # Save mapping
    import json
    with open(data_dir / "class_mapping.json", 'w') as f:
        json.dump(class_to_idx, f, indent=2)
    
    print(f"Created class mapping with {len(classes)} classes")
    return class_to_idx

if __name__ == "__main__":
    print("Setting up Food-101 dataset...")
    setup_food101_dataset()
    create_class_mapping()
    print("Dataset setup complete!") 