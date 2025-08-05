"""
Training utilities for food recognition model
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import StepLR, CosineAnnealingLR
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import json
from pathlib import Path
import wandb
from typing import Dict, List, Tuple, Optional

class Trainer:
    """Training class for food recognition model"""
    
    def __init__(self, 
                 model: nn.Module,
                 train_loader,
                 val_loader,
                 test_loader,
                 config,
                 device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        Args:
            model: Food recognition model
            train_loader: Training data loader
            val_loader: Validation data loader
            test_loader: Test data loader
            config: Training configuration
            device: Device to train on
        """
        self.model = model.to(device)
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.test_loader = test_loader
        self.config = config
        self.device = device
        
        # Loss functions
        self.classification_criterion = nn.CrossEntropyLoss()
        if config.macro_estimation_enabled:
            self.macro_criterion = nn.MSELoss()
        
        # Optimizer
        self.optimizer = optim.AdamW(
            self.model.parameters(),
            lr=config.learning_rate,
            weight_decay=config.weight_decay
        )
        
        # Learning rate scheduler
        self.scheduler = StepLR(
            self.optimizer,
            step_size=config.scheduler_step_size,
            gamma=config.scheduler_gamma
        )
        
        # Training history
        self.train_history = {
            'loss': [],
            'accuracy': [],
            'val_loss': [],
            'val_accuracy': []
        }
        
        # Best model tracking
        self.best_val_accuracy = 0.0
        self.best_model_path = None
    
    def train_epoch(self) -> Dict[str, float]:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0
        
        progress_bar = tqdm(self.train_loader, desc="Training")
        
        for batch_idx, (data, target) in enumerate(progress_bar):
            data, target = data.to(self.device), target.to(self.device)
            
            self.optimizer.zero_grad()
            
            # Forward pass
            outputs = self.model(data)
            
            # Calculate loss
            classification_loss = self.classification_criterion(outputs['classification'], target)
            
            if self.config.macro_estimation_enabled and outputs['macros'] is not None:
                # For macro estimation, we would need macro labels
                # For now, we'll just use classification loss
                loss = classification_loss
            else:
                loss = classification_loss
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            # Statistics
            total_loss += loss.item()
            pred = outputs['classification'].argmax(dim=1, keepdim=True)
            correct += pred.eq(target.view_as(pred)).sum().item()
            total += target.size(0)
            
            # Update progress bar
            progress_bar.set_postfix({
                'Loss': f'{loss.item():.4f}',
                'Acc': f'{100. * correct / total:.2f}%'
            })
        
        epoch_loss = total_loss / len(self.train_loader)
        epoch_accuracy = 100. * correct / total
        
        return {
            'loss': epoch_loss,
            'accuracy': epoch_accuracy
        }
    
    def validate_epoch(self) -> Dict[str, float]:
        """Validate for one epoch"""
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in tqdm(self.val_loader, desc="Validation"):
                data, target = data.to(self.device), target.to(self.device)
                
                # Forward pass
                outputs = self.model(data)
                
                # Calculate loss
                classification_loss = self.classification_criterion(outputs['classification'], target)
                loss = classification_loss
                
                # Statistics
                total_loss += loss.item()
                pred = outputs['classification'].argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
                total += target.size(0)
        
        epoch_loss = total_loss / len(self.val_loader)
        epoch_accuracy = 100. * correct / total
        
        return {
            'loss': epoch_loss,
            'accuracy': epoch_accuracy
        }
    
    def train(self, num_epochs: int, save_dir: str = "models"):
        """Train the model"""
        save_path = Path(save_dir)
        save_path.mkdir(exist_ok=True)
        
        print(f"Starting training for {num_epochs} epochs...")
        print(f"Device: {self.device}")
        
        for epoch in range(num_epochs):
            print(f"\nEpoch {epoch + 1}/{num_epochs}")
            
            # Training
            train_metrics = self.train_epoch()
            
            # Validation
            val_metrics = self.validate_epoch()
            
            # Update learning rate
            self.scheduler.step()
            
            # Log metrics
            print(f"Train Loss: {train_metrics['loss']:.4f}, Train Acc: {train_metrics['accuracy']:.2f}%")
            print(f"Val Loss: {val_metrics['loss']:.4f}, Val Acc: {val_metrics['accuracy']:.2f}%")
            
            # Save to history
            self.train_history['loss'].append(train_metrics['loss'])
            self.train_history['accuracy'].append(train_metrics['accuracy'])
            self.train_history['val_loss'].append(val_metrics['loss'])
            self.train_history['val_accuracy'].append(val_metrics['accuracy'])
            
            # Save best model
            if val_metrics['accuracy'] > self.best_val_accuracy:
                self.best_val_accuracy = val_metrics['accuracy']
                best_model_path = save_path / f"best_model_epoch_{epoch+1}.pth"
                self.save_model(best_model_path)
                self.best_model_path = best_model_path
                print(f"New best model saved with validation accuracy: {self.best_val_accuracy:.2f}%")
            
            # Save checkpoint
            if (epoch + 1) % 10 == 0:
                checkpoint_path = save_path / f"checkpoint_epoch_{epoch+1}.pth"
                self.save_checkpoint(checkpoint_path, epoch)
        
        # Save final model
        final_model_path = save_path / "final_model.pth"
        self.save_model(final_model_path)
        
        print(f"\nTraining completed!")
        print(f"Best validation accuracy: {self.best_val_accuracy:.2f}%")
    
    def save_model(self, path: str):
        """Save model"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'config': self.config,
            'train_history': self.train_history
        }, path)
    
    def save_checkpoint(self, path: str, epoch: int):
        """Save training checkpoint"""
        torch.save({
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'train_history': self.train_history,
            'best_val_accuracy': self.best_val_accuracy,
            'config': self.config
        }, path)
    
    def load_checkpoint(self, path: str):
        """Load training checkpoint"""
        checkpoint = torch.load(path, map_location=self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        self.train_history = checkpoint['train_history']
        self.best_val_accuracy = checkpoint['best_val_accuracy']
        
        return checkpoint['epoch']
    
    def evaluate(self, loader, class_names: List[str] = None) -> Dict[str, float]:
        """Evaluate model on given data loader"""
        self.model.eval()
        all_predictions = []
        all_targets = []
        total_loss = 0.0
        
        with torch.no_grad():
            for data, target in tqdm(loader, desc="Evaluating"):
                data, target = data.to(self.device), target.to(self.device)
                
                outputs = self.model(data)
                loss = self.classification_criterion(outputs['classification'], target)
                
                total_loss += loss.item()
                pred = outputs['classification'].argmax(dim=1)
                
                all_predictions.extend(pred.cpu().numpy())
                all_targets.extend(target.cpu().numpy())
        
        # Calculate metrics
        accuracy = accuracy_score(all_targets, all_predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            all_targets, all_predictions, average='weighted'
        )
        
        metrics = {
            'loss': total_loss / len(loader),
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
        
        # Confusion matrix
        cm = confusion_matrix(all_targets, all_predictions)
        
        return metrics, cm, all_predictions, all_targets
    
    def plot_training_history(self, save_path: str = None):
        """Plot training history"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Loss plot
        ax1.plot(self.train_history['loss'], label='Train Loss')
        ax1.plot(self.train_history['val_loss'], label='Validation Loss')
        ax1.set_title('Training and Validation Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Accuracy plot
        ax2.plot(self.train_history['accuracy'], label='Train Accuracy')
        ax2.plot(self.train_history['val_accuracy'], label='Validation Accuracy')
        ax2.set_title('Training and Validation Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy (%)')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_confusion_matrix(self, cm, class_names: List[str], save_path: str = None):
        """Plot confusion matrix"""
        plt.figure(figsize=(20, 16))
        
        # Use only first 20 classes for better visualization
        if len(class_names) > 20:
            cm = cm[:20, :20]
            class_names = class_names[:20]
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=class_names, yticklabels=class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

def create_trainer(model, train_loader, val_loader, test_loader, config):
    """Create trainer instance"""
    return Trainer(model, train_loader, val_loader, test_loader, config) 