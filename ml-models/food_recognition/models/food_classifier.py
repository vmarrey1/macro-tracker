"""
Food classification model architectures
"""

import torch
import torch.nn as nn
import torchvision.models as models
import timm
from typing import Optional, Dict, Any

class FoodClassifier(nn.Module):
    """Food classification model based on pre-trained architectures"""
    
    def __init__(self, 
                 model_name: str = "resnet50",
                 num_classes: int = 101,
                 pretrained: bool = True,
                 dropout_rate: float = 0.5,
                 freeze_backbone: bool = False):
        """
        Args:
            model_name: Name of the backbone model
            num_classes: Number of food classes
            pretrained: Whether to use pretrained weights
            dropout_rate: Dropout rate for regularization
            freeze_backbone: Whether to freeze backbone layers
        """
        super(FoodClassifier, self).__init__()
        
        self.model_name = model_name
        self.num_classes = num_classes
        
        # Load backbone model
        if model_name.startswith("resnet"):
            self.backbone = self._get_resnet_model(model_name, pretrained)
            feature_dim = self.backbone.fc.in_features
            self.backbone.fc = nn.Identity()  # Remove classifier
        elif model_name.startswith("efficientnet"):
            self.backbone = timm.create_model(model_name, pretrained=pretrained, num_classes=0)
            feature_dim = self.backbone.num_features
        elif model_name.startswith("vit"):
            self.backbone = timm.create_model(model_name, pretrained=pretrained, num_classes=0)
            feature_dim = self.backbone.num_features
        else:
            raise ValueError(f"Unsupported model: {model_name}")
        
        # Freeze backbone if requested
        if freeze_backbone:
            for param in self.backbone.parameters():
                param.requires_grad = False
        
        # Classifier head
        self.classifier = nn.Sequential(
            nn.Dropout(dropout_rate),
            nn.Linear(feature_dim, 512),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(512, num_classes)
        )
        
        # Initialize weights
        self._initialize_weights()
    
    def _get_resnet_model(self, model_name: str, pretrained: bool):
        """Get ResNet model"""
        model_map = {
            "resnet18": models.resnet18,
            "resnet34": models.resnet34,
            "resnet50": models.resnet50,
            "resnet101": models.resnet101,
            "resnet152": models.resnet152,
        }
        
        if model_name not in model_map:
            raise ValueError(f"Unsupported ResNet model: {model_name}")
        
        return model_map[model_name](pretrained=pretrained)
    
    def _initialize_weights(self):
        """Initialize classifier weights"""
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
    
    def forward(self, x):
        """Forward pass"""
        features = self.backbone(x)
        output = self.classifier(features)
        return output
    
    def get_features(self, x):
        """Get feature representation"""
        return self.backbone(x)

class EnsembleFoodClassifier(nn.Module):
    """Ensemble of multiple food classification models"""
    
    def __init__(self, 
                 model_configs: list,
                 num_classes: int = 101,
                 ensemble_method: str = "average"):
        """
        Args:
            model_configs: List of model configurations
            num_classes: Number of food classes
            ensemble_method: Ensemble method ('average', 'weighted', 'voting')
        """
        super(EnsembleFoodClassifier, self).__init__()
        
        self.models = nn.ModuleList()
        self.ensemble_method = ensemble_method
        
        for config in model_configs:
            model = FoodClassifier(
                model_name=config["model_name"],
                num_classes=num_classes,
                pretrained=config.get("pretrained", True),
                dropout_rate=config.get("dropout_rate", 0.5)
            )
            self.models.append(model)
        
        if ensemble_method == "weighted":
            self.weights = nn.Parameter(torch.ones(len(self.models)))
    
    def forward(self, x):
        """Forward pass with ensemble"""
        outputs = []
        
        for model in self.models:
            output = model(x)
            outputs.append(output)
        
        if self.ensemble_method == "average":
            return torch.stack(outputs).mean(dim=0)
        elif self.ensemble_method == "weighted":
            weights = torch.softmax(self.weights, dim=0)
            weighted_outputs = [w * out for w, out in zip(weights, outputs)]
            return torch.stack(weighted_outputs).sum(dim=0)
        elif self.ensemble_method == "voting":
            # Hard voting based on predictions
            predictions = [torch.argmax(out, dim=1) for out in outputs]
            return torch.stack(predictions).mode(dim=0)[0]
        else:
            raise ValueError(f"Unsupported ensemble method: {self.ensemble_method}")

class MacroEstimator(nn.Module):
    """Neural network for estimating macro nutrients from food images"""
    
    def __init__(self, 
                 feature_dim: int = 2048,
                 hidden_dim: int = 512,
                 dropout_rate: float = 0.3):
        """
        Args:
            feature_dim: Input feature dimension
            hidden_dim: Hidden layer dimension
            dropout_rate: Dropout rate
        """
        super(MacroEstimator, self).__init__()
        
        self.regressor = nn.Sequential(
            nn.Linear(feature_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_dim // 2, 5)  # calories, protein, carbs, fat, fiber
        )
        
        self._initialize_weights()
    
    def _initialize_weights(self):
        """Initialize weights"""
        for m in self.regressor.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
    
    def forward(self, features):
        """Forward pass"""
        return self.regressor(features)

class FoodRecognitionModel(nn.Module):
    """Complete food recognition model with classification and macro estimation"""
    
    def __init__(self,
                 classifier: FoodClassifier,
                 macro_estimator: Optional[MacroEstimator] = None,
                 use_macro_estimation: bool = True):
        """
        Args:
            classifier: Food classification model
            macro_estimator: Macro estimation model
            use_macro_estimation: Whether to use macro estimation
        """
        super(FoodRecognitionModel, self).__init__()
        
        self.classifier = classifier
        self.use_macro_estimation = use_macro_estimation
        
        if use_macro_estimation and macro_estimator is not None:
            self.macro_estimator = macro_estimator
        else:
            self.macro_estimator = None
    
    def forward(self, x):
        """Forward pass"""
        # Get features from classifier backbone
        features = self.classifier.get_features(x)
        
        # Classification output
        classification_output = self.classifier(x)
        
        # Macro estimation output
        macro_output = None
        if self.use_macro_estimation and self.macro_estimator is not None:
            macro_output = self.macro_estimator(features)
        
        return {
            'classification': classification_output,
            'macros': macro_output,
            'features': features
        }
    
    def predict(self, x):
        """Prediction with post-processing"""
        outputs = self.forward(x)
        
        # Get classification probabilities
        classification_probs = torch.softmax(outputs['classification'], dim=1)
        
        # Get predicted class
        predicted_class = torch.argmax(classification_probs, dim=1)
        
        return {
            'class': predicted_class,
            'probabilities': classification_probs,
            'macros': outputs['macros']
        }

def create_model(model_name: str = "resnet50",
                num_classes: int = 101,
                pretrained: bool = True,
                dropout_rate: float = 0.5,
                use_macro_estimation: bool = True) -> FoodRecognitionModel:
    """Create a food recognition model"""
    
    # Create classifier
    classifier = FoodClassifier(
        model_name=model_name,
        num_classes=num_classes,
        pretrained=pretrained,
        dropout_rate=dropout_rate
    )
    
    # Create macro estimator if needed
    macro_estimator = None
    if use_macro_estimation:
        # Get feature dimension from classifier
        if model_name.startswith("resnet"):
            feature_dim = 2048 if "50" in model_name or "101" in model_name or "152" in model_name else 512
        elif model_name.startswith("efficientnet"):
            feature_dim = 1280  # EfficientNet-B0
        else:
            feature_dim = 768  # Default for other models
        
        macro_estimator = MacroEstimator(feature_dim=feature_dim)
    
    # Create complete model
    model = FoodRecognitionModel(
        classifier=classifier,
        macro_estimator=macro_estimator,
        use_macro_estimation=use_macro_estimation
    )
    
    return model 