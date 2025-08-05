# Food Recognition ML System

A comprehensive machine learning system for food image recognition and macro nutrient estimation using PyTorch, OpenCV, and state-of-the-art computer vision models.

## 🍽️ Features

- **Food Classification**: Recognize 101 different food categories from the Food-101 dataset
- **Macro Estimation**: Estimate calories, protein, carbs, fat, and fiber content
- **Multiple Architectures**: Support for ResNet, EfficientNet, and Vision Transformer models
- **Advanced Augmentation**: Albumentations library for robust training
- **Ensemble Methods**: Combine multiple models for improved accuracy
- **Comprehensive Evaluation**: Detailed metrics and visualization tools

## 📁 Project Structure

```
ml-models/
├── food_recognition/
│   ├── config.py                 # Configuration settings
│   ├── data/                     # Dataset directory
│   ├── models/                   # Model architectures
│   │   └── food_classifier.py
│   ├── utils/                    # Utility functions
│   │   ├── dataset.py
│   │   └── training_utils.py
│   ├── training/                 # Training scripts
│   │   └── train.py
│   └── scripts/                  # Utility scripts
│       ├── download_data.py
│       └── inference.py
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd ml-models
pip install -r requirements.txt
```

### 2. Download and Prepare Dataset

```bash
cd food_recognition
python scripts/download_data.py
```

This will:
- Download the Food-101 dataset (~6GB)
- Organize images into train/val/test splits
- Create class mapping for 101 food categories

### 3. Train the Model

```bash
python training/train.py \
    --data_dir data/organized \
    --model_name resnet50 \
    --batch_size 32 \
    --num_epochs 50 \
    --learning_rate 0.001 \
    --use_albumentations \
    --save_dir models
```

### 4. Run Inference

```bash
python scripts/inference.py \
    --model_path models/best_model_epoch_50.pth \
    --class_mapping models/class_mapping.json \
    --image_path path/to/your/food/image.jpg
```

## 🏗️ Model Architecture

### Food Classifier
- **Backbone**: Pre-trained ResNet, EfficientNet, or Vision Transformer
- **Classifier Head**: Custom fully connected layers with dropout
- **Output**: 101-class classification probabilities

### Macro Estimator (Optional)
- **Input**: Features from classifier backbone
- **Architecture**: Multi-layer perceptron
- **Output**: 5 values (calories, protein, carbs, fat, fiber)

### Complete Model
```python
FoodRecognitionModel:
├── FoodClassifier (ResNet50 + Custom Head)
├── MacroEstimator (MLP for macro prediction)
└── Combined outputs for classification + macro estimation
```

## 📊 Dataset

### Food-101 Dataset
- **101 food categories** (pizza, sushi, hamburger, etc.)
- **101,000 images** total
- **1,000 images per class**
- **High-quality food photography**

### Data Organization
```
data/organized/
├── train/
│   ├── apple_pie/
│   ├── baby_back_ribs/
│   └── ...
├── val/
│   ├── apple_pie/
│   ├── baby_back_ribs/
│   └── ...
└── test/
    ├── apple_pie/
    ├── baby_back_ribs/
    └── ...
```

## 🎯 Training Configuration

### Model Options
- `resnet18`, `resnet34`, `resnet50`, `resnet101`, `resnet152`
- `efficientnet_b0`, `efficientnet_b1`, `efficientnet_b2`
- `vit_base_patch16_224`, `vit_large_patch16_224`

### Training Parameters
- **Batch Size**: 32 (adjustable)
- **Learning Rate**: 0.001 with StepLR scheduler
- **Epochs**: 50 (configurable)
- **Image Size**: 224x224
- **Augmentation**: Horizontal flip, rotation, color jitter

### Advanced Features
- **Albumentations**: Advanced augmentation pipeline
- **Macro Estimation**: Optional macro nutrient prediction
- **Ensemble Training**: Combine multiple models
- **Transfer Learning**: Pre-trained ImageNet weights

## 📈 Performance Metrics

### Classification Metrics
- **Accuracy**: Overall classification accuracy
- **Precision**: Per-class precision scores
- **Recall**: Per-class recall scores
- **F1-Score**: Harmonic mean of precision and recall

### Macro Estimation Metrics
- **MSE**: Mean squared error for macro predictions
- **MAE**: Mean absolute error for macro predictions
- **R² Score**: Coefficient of determination

## 🔧 Usage Examples

### Basic Training
```python
from training.train import main

# Train ResNet50 model
main([
    '--data_dir', 'data/organized',
    '--model_name', 'resnet50',
    '--batch_size', '32',
    '--num_epochs', '50',
    '--save_dir', 'models'
])
```

### Custom Model Creation
```python
from models.food_classifier import create_model

# Create model with macro estimation
model = create_model(
    model_name="resnet50",
    num_classes=101,
    pretrained=True,
    use_macro_estimation=True
)
```

### Inference
```python
from scripts.inference import FoodRecognitionPredictor

# Load trained model
predictor = FoodRecognitionPredictor(
    model_path="models/best_model.pth",
    class_mapping_path="models/class_mapping.json"
)

# Analyze food image
result = predictor.analyze_image("food_image.jpg")
print(f"Food: {result['food_name']}")
print(f"Calories: {result['macros']['calories']} kcal")
```

## 📊 Results Visualization

### Training History
- Loss curves (train/validation)
- Accuracy curves (train/validation)
- Learning rate scheduling

### Evaluation Plots
- Confusion matrix
- Per-class accuracy
- Macro estimation error analysis

### Example Output
```
=== Food Recognition Results ===
Food: Pizza
Confidence: 94.5%

=== Macro Nutrients (per serving) ===
Calories: 280.0 kcal
Protein: 12.0g
Carbohydrates: 35.0g
Fat: 12.0g
Fiber: 2.0g

=== Top 5 Predictions ===
1. Pizza (94.5%)
2. Lasagna (3.2%)
3. Macaroni And Cheese (1.1%)
4. Ravioli (0.8%)
5. Spaghetti Bolognese (0.4%)
```

## 🛠️ Advanced Features

### Ensemble Models
```python
from models.food_classifier import EnsembleFoodClassifier

# Create ensemble of multiple models
model_configs = [
    {"model_name": "resnet50", "dropout_rate": 0.5},
    {"model_name": "efficientnet_b0", "dropout_rate": 0.3},
    {"model_name": "vit_base_patch16_224", "dropout_rate": 0.4}
]

ensemble = EnsembleFoodClassifier(
    model_configs=model_configs,
    num_classes=101,
    ensemble_method="weighted"
)
```

### Custom Data Loading
```python
from utils.dataset import create_data_loaders

# Create data loaders with custom settings
train_loader, val_loader, test_loader, class_mapping = create_data_loaders(
    data_dir="data/organized",
    batch_size=64,
    image_size=224,
    use_albumentations=True
)
```

### Model Evaluation
```python
from utils.training_utils import Trainer

# Evaluate trained model
trainer = Trainer(model, train_loader, val_loader, test_loader, config)
metrics, cm, preds, targets = trainer.evaluate(test_loader)

print(f"Test Accuracy: {metrics['accuracy']:.4f}")
print(f"Test F1-Score: {metrics['f1_score']:.4f}")
```

## 🔍 Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size: `--batch_size 16`
   - Use smaller model: `--model_name resnet18`

2. **Slow Training**
   - Increase num_workers: `--num_workers 8`
   - Use mixed precision training
   - Enable GPU acceleration

3. **Poor Accuracy**
   - Increase training epochs
   - Use data augmentation: `--use_albumentations`
   - Try different learning rates
   - Use ensemble models

### Performance Tips

- **GPU Training**: Use CUDA-enabled GPU for faster training
- **Data Augmentation**: Enable Albumentations for better generalization
- **Transfer Learning**: Use pre-trained models for better results
- **Ensemble Methods**: Combine multiple models for improved accuracy

## 📚 Dependencies

### Core Libraries
- **PyTorch**: Deep learning framework
- **TorchVision**: Computer vision utilities
- **OpenCV**: Image processing
- **PIL**: Image loading and manipulation

### Data Processing
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Albumentations**: Advanced image augmentation

### Visualization
- **Matplotlib**: Plotting
- **Seaborn**: Statistical visualization

### Model Libraries
- **timm**: Pre-trained models
- **transformers**: Vision transformers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Food-101 Dataset**: ETH Zurich Computer Vision Lab
- **PyTorch**: Facebook AI Research
- **Albumentations**: Intel Corporation
- **timm**: Ross Wightman

---

**Note**: This system is designed for educational and research purposes. For production use, consider additional validation, testing, and deployment considerations. 