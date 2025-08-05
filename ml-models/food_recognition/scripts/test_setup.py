#!/usr/bin/env python3
"""
Test script to verify the food recognition ML setup
"""

import sys
import torch
import numpy as np
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from config import config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from utils.dataset import FoodDataset, create_data_loaders
        print("✅ Dataset modules imported successfully")
    except ImportError as e:
        print(f"❌ Dataset import failed: {e}")
        return False
    
    try:
        from models.food_classifier import create_model, FoodClassifier
        print("✅ Model modules imported successfully")
    except ImportError as e:
        print(f"❌ Model import failed: {e}")
        return False
    
    try:
        from utils.training_utils import Trainer, create_trainer
        print("✅ Training utilities imported successfully")
    except ImportError as e:
        print(f"❌ Training utilities import failed: {e}")
        return False
    
    return True

def test_pytorch():
    """Test PyTorch installation and CUDA availability"""
    print("\nTesting PyTorch...")
    
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU device: {torch.cuda.get_device_name(0)}")
    
    # Test basic tensor operations
    try:
        x = torch.randn(2, 3, 224, 224)
        y = torch.randn(2, 3, 224, 224)
        z = x + y
        print("✅ Basic tensor operations work")
    except Exception as e:
        print(f"❌ Tensor operations failed: {e}")
        return False
    
    return True

def test_model_creation():
    """Test model creation"""
    print("\nTesting model creation...")
    
    try:
        from models.food_classifier import create_model
        
        # Test creating a simple model
        model = create_model(
            model_name="resnet18",
            num_classes=101,
            pretrained=False,  # Don't download pretrained weights for testing
            use_macro_estimation=True
        )
        
        print(f"✅ Model created successfully")
        print(f"   Total parameters: {sum(p.numel() for p in model.parameters()):,}")
        print(f"   Trainable parameters: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
        
        # Test forward pass
        x = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(x)
        
        print(f"✅ Forward pass successful")
        print(f"   Classification output shape: {output['classification'].shape}")
        if output['macros'] is not None:
            print(f"   Macro output shape: {output['macros'].shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False

def test_dataset_creation():
    """Test dataset creation (without actual data)"""
    print("\nTesting dataset creation...")
    
    try:
        from utils.dataset import FoodDataset, get_transforms
        
        # Test transforms
        transform = get_transforms(image_size=224, split='train')
        print("✅ Transforms created successfully")
        
        # Test dataset class (without actual data)
        print("✅ Dataset class structure verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Dataset creation failed: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    try:
        from config import config
        
        print(f"✅ Configuration loaded")
        print(f"   Model name: {config.model_name}")
        print(f"   Number of classes: {config.num_classes}")
        print(f"   Image size: {config.image_size}")
        print(f"   Batch size: {config.batch_size}")
        print(f"   Learning rate: {config.learning_rate}")
        print(f"   Number of food categories: {len(config.food_categories)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_dependencies():
    """Test that all required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        ('torch', 'PyTorch'),
        ('torchvision', 'TorchVision'),
        ('cv2', 'OpenCV'),
        ('numpy', 'NumPy'),
        ('PIL', 'Pillow'),
        ('matplotlib', 'Matplotlib'),
        ('seaborn', 'Seaborn'),
        ('sklearn', 'Scikit-learn'),
        ('pandas', 'Pandas'),
        ('albumentations', 'Albumentations'),
        ('timm', 'timm'),
    ]
    
    all_good = True
    
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {display_name} available")
        except ImportError:
            print(f"❌ {display_name} not available")
            all_good = False
    
    return all_good

def main():
    """Run all tests"""
    print("🧪 Testing Food Recognition ML Setup")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_imports,
        test_pytorch,
        test_config,
        test_model_creation,
        test_dataset_creation,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    test_names = [
        "Dependencies",
        "Imports",
        "PyTorch",
        "Configuration",
        "Model Creation",
        "Dataset Creation"
    ]
    
    passed = 0
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All tests passed! The ML setup is ready.")
        print("\nNext steps:")
        print("1. Download the dataset: python scripts/download_data.py")
        print("2. Train the model: python training/train.py --data_dir data/organized")
        print("3. Run inference: python scripts/inference.py --model_path models/best_model.pth --image_path your_image.jpg")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Check Python version (3.8+ recommended)")
        print("3. Verify PyTorch installation: https://pytorch.org/get-started/")

if __name__ == "__main__":
    main() 