#!/usr/bin/env python3
"""
Main training script for food recognition model
"""

import os
import sys
import argparse
import torch
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import config
from utils.dataset import create_data_loaders
from models.food_classifier import create_model
from utils.training_utils import create_trainer

def main():
    parser = argparse.ArgumentParser(description='Train food recognition model')
    parser.add_argument('--data_dir', type=str, default='data/organized',
                       help='Path to organized dataset directory')
    parser.add_argument('--model_name', type=str, default='resnet50',
                       help='Model architecture to use')
    parser.add_argument('--batch_size', type=int, default=32,
                       help='Batch size for training')
    parser.add_argument('--num_epochs', type=int, default=50,
                       help='Number of training epochs')
    parser.add_argument('--learning_rate', type=float, default=0.001,
                       help='Learning rate')
    parser.add_argument('--image_size', type=int, default=224,
                       help='Input image size')
    parser.add_argument('--use_albumentations', action='store_true',
                       help='Use Albumentations for augmentation')
    parser.add_argument('--macro_estimation', action='store_true',
                       help='Enable macro estimation')
    parser.add_argument('--save_dir', type=str, default='models',
                       help='Directory to save models')
    parser.add_argument('--resume', type=str, default=None,
                       help='Path to checkpoint to resume from')
    
    args = parser.parse_args()
    
    # Update config with command line arguments
    config.model_name = args.model_name
    config.batch_size = args.batch_size
    config.num_epochs = args.num_epochs
    config.learning_rate = args.learning_rate
    config.image_size = args.image_size
    config.macro_estimation_enabled = args.macro_estimation
    
    print("Configuration:")
    print(f"Model: {config.model_name}")
    print(f"Batch size: {config.batch_size}")
    print(f"Learning rate: {config.learning_rate}")
    print(f"Image size: {config.image_size}")
    print(f"Macro estimation: {config.macro_estimation_enabled}")
    print(f"Albumentations: {args.use_albumentations}")
    
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Create data loaders
    print("Creating data loaders...")
    train_loader, val_loader, test_loader, class_mapping = create_data_loaders(
        data_dir=args.data_dir,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
        image_size=config.image_size,
        use_albumentations=args.use_albumentations
    )
    
    print(f"Number of classes: {len(class_mapping)}")
    print(f"Training samples: {len(train_loader.dataset)}")
    print(f"Validation samples: {len(val_loader.dataset)}")
    print(f"Test samples: {len(test_loader.dataset)}")
    
    # Create model
    print("Creating model...")
    model = create_model(
        model_name=config.model_name,
        num_classes=len(class_mapping),
        pretrained=config.pretrained,
        dropout_rate=config.dropout_rate,
        use_macro_estimation=config.macro_estimation_enabled
    )
    
    # Print model summary
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    
    # Create trainer
    trainer = create_trainer(model, train_loader, val_loader, test_loader, config)
    
    # Resume training if checkpoint provided
    if args.resume:
        print(f"Resuming from checkpoint: {args.resume}")
        epoch = trainer.load_checkpoint(args.resume)
        print(f"Resumed from epoch: {epoch}")
    
    # Create save directory
    save_dir = Path(args.save_dir)
    save_dir.mkdir(exist_ok=True)
    
    # Train the model
    print("Starting training...")
    trainer.train(num_epochs=config.num_epochs, save_dir=str(save_dir))
    
    # Evaluate on test set
    print("Evaluating on test set...")
    test_metrics, test_cm, test_preds, test_targets = trainer.evaluate(
        test_loader, list(class_mapping.keys())
    )
    
    print("Test Results:")
    for metric, value in test_metrics.items():
        print(f"{metric}: {value:.4f}")
    
    # Plot training history
    print("Plotting training history...")
    trainer.plot_training_history(save_path=str(save_dir / "training_history.png"))
    
    # Plot confusion matrix
    print("Plotting confusion matrix...")
    trainer.plot_confusion_matrix(
        test_cm, 
        list(class_mapping.keys()),
        save_path=str(save_dir / "confusion_matrix.png")
    )
    
    # Save class mapping
    import json
    with open(save_dir / "class_mapping.json", 'w') as f:
        json.dump(class_mapping, f, indent=2)
    
    print("Training completed successfully!")
    print(f"Best validation accuracy: {trainer.best_val_accuracy:.2f}%")
    print(f"Test accuracy: {test_metrics['accuracy']:.4f}")

if __name__ == "__main__":
    main() 