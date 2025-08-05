#!/usr/bin/env python3
"""
Inference script for food recognition and macro estimation
"""

import os
import sys
import torch
import numpy as np
import cv2
from PIL import Image
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import config
from models.food_classifier import create_model
from utils.dataset import get_transforms

class FoodRecognitionPredictor:
    """Food recognition and macro estimation predictor"""
    
    def __init__(self, 
                 model_path: str,
                 class_mapping_path: str,
                 device: str = "cuda" if torch.cuda.is_available() else "cpu"):
        """
        Args:
            model_path: Path to trained model
            class_mapping_path: Path to class mapping JSON file
            device: Device to run inference on
        """
        self.device = device
        self.model_path = model_path
        self.class_mapping_path = class_mapping_path
        
        # Load class mapping
        with open(class_mapping_path, 'r') as f:
            self.class_mapping = json.load(f)
        
        self.idx_to_class = {idx: class_name for class_name, idx in self.class_mapping.items()}
        
        # Load model
        self.model = self._load_model()
        self.model.eval()
        
        # Load transforms
        self.transform = get_transforms(image_size=config.image_size, split='test')
        
        print(f"Model loaded from: {model_path}")
        print(f"Number of classes: {len(self.class_mapping)}")
        print(f"Device: {device}")
    
    def _load_model(self):
        """Load trained model"""
        # Create model architecture
        model = create_model(
            model_name=config.model_name,
            num_classes=len(self.class_mapping),
            pretrained=False,  # Don't load pretrained weights
            dropout_rate=config.dropout_rate,
            use_macro_estimation=config.macro_estimation_enabled
        )
        
        # Load trained weights
        checkpoint = torch.load(self.model_path, map_location=self.device)
        model.load_state_dict(checkpoint['model_state_dict'])
        
        return model.to(self.device)
    
    def preprocess_image(self, image_path: str) -> torch.Tensor:
        """Preprocess image for inference"""
        # Load image
        if isinstance(image_path, str):
            image = Image.open(image_path).convert('RGB')
        else:
            image = image_path
        
        # Apply transforms
        image_tensor = self.transform(image)
        
        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)
        
        return image_tensor.to(self.device)
    
    def predict(self, image_path: str, top_k: int = 5) -> Dict:
        """Predict food class and macros for an image"""
        # Preprocess image
        image_tensor = self.preprocess_image(image_path)
        
        # Run inference
        with torch.no_grad():
            outputs = self.model(image_tensor)
        
        # Get classification results
        classification_probs = torch.softmax(outputs['classification'], dim=1)
        top_probs, top_indices = torch.topk(classification_probs, top_k, dim=1)
        
        # Convert to numpy
        top_probs = top_probs.cpu().numpy()[0]
        top_indices = top_indices.cpu().numpy()[0]
        
        # Get predicted class names and probabilities
        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            class_name = self.idx_to_class[idx]
            predictions.append({
                'class': class_name,
                'probability': float(prob),
                'macros': self._get_macros_for_class(class_name)
            })
        
        # Get macro estimation if available
        estimated_macros = None
        if config.macro_estimation_enabled and outputs['macros'] is not None:
            estimated_macros = outputs['macros'].cpu().numpy()[0]
            estimated_macros = {
                'calories': float(estimated_macros[0]),
                'protein': float(estimated_macros[1]),
                'carbs': float(estimated_macros[2]),
                'fat': float(estimated_macros[3]),
                'fiber': float(estimated_macros[4])
            }
        
        return {
            'predictions': predictions,
            'estimated_macros': estimated_macros,
            'top_prediction': predictions[0] if predictions else None
        }
    
    def _get_macros_for_class(self, class_name: str) -> Dict[str, float]:
        """Get macro information for a food class"""
        if class_name in config.food_categories:
            return config.food_categories[class_name]
        else:
            # Return default values if class not found
            return {
                'calories': 0.0,
                'protein': 0.0,
                'carbs': 0.0,
                'fat': 0.0,
                'fiber': 0.0
            }
    
    def predict_batch(self, image_paths: List[str], top_k: int = 5) -> List[Dict]:
        """Predict for multiple images"""
        results = []
        
        for image_path in image_paths:
            result = self.predict(image_path, top_k)
            results.append(result)
        
        return results
    
    def analyze_image(self, image_path: str) -> Dict:
        """Comprehensive image analysis"""
        prediction = self.predict(image_path)
        
        # Get the top prediction
        top_pred = prediction['top_prediction']
        
        if top_pred:
            analysis = {
                'food_name': top_pred['class'].replace('_', ' ').title(),
                'confidence': f"{top_pred['probability']:.2%}",
                'macros': top_pred['macros'],
                'all_predictions': prediction['predictions'],
                'estimated_macros': prediction['estimated_macros']
            }
        else:
            analysis = {
                'food_name': 'Unknown',
                'confidence': '0%',
                'macros': {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0},
                'all_predictions': [],
                'estimated_macros': None
            }
        
        return analysis

def main():
    """Example usage of the predictor"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Food recognition inference')
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to trained model')
    parser.add_argument('--class_mapping', type=str, required=True,
                       help='Path to class mapping JSON file')
    parser.add_argument('--image_path', type=str, required=True,
                       help='Path to image to analyze')
    parser.add_argument('--top_k', type=int, default=5,
                       help='Number of top predictions to return')
    
    args = parser.parse_args()
    
    # Create predictor
    predictor = FoodRecognitionPredictor(
        model_path=args.model_path,
        class_mapping_path=args.class_mapping
    )
    
    # Analyze image
    analysis = predictor.analyze_image(args.image_path)
    
    # Print results
    print("\n=== Food Recognition Results ===")
    print(f"Food: {analysis['food_name']}")
    print(f"Confidence: {analysis['confidence']}")
    
    print("\n=== Macro Nutrients (per serving) ===")
    macros = analysis['macros']
    print(f"Calories: {macros['calories']:.1f} kcal")
    print(f"Protein: {macros['protein']:.1f}g")
    print(f"Carbohydrates: {macros['carbs']:.1f}g")
    print(f"Fat: {macros['fat']:.1f}g")
    print(f"Fiber: {macros['fiber']:.1f}g")
    
    if analysis['estimated_macros']:
        print("\n=== Estimated Macros (from model) ===")
        est_macros = analysis['estimated_macros']
        print(f"Calories: {est_macros['calories']:.1f} kcal")
        print(f"Protein: {est_macros['protein']:.1f}g")
        print(f"Carbohydrates: {est_macros['carbs']:.1f}g")
        print(f"Fat: {est_macros['fat']:.1f}g")
        print(f"Fiber: {est_macros['fiber']:.1f}g")
    
    print("\n=== Top 5 Predictions ===")
    for i, pred in enumerate(analysis['all_predictions'][:5]):
        print(f"{i+1}. {pred['class'].replace('_', ' ').title()} ({pred['probability']:.2%})")

if __name__ == "__main__":
    main() 