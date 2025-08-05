import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ModelConfig:
    """Configuration for the food recognition model"""
    
    # Model parameters
    model_name: str = "resnet50"
    num_classes: int = 101  # Food-101 dataset has 101 classes
    pretrained: bool = True
    dropout_rate: float = 0.5
    
    # Training parameters
    batch_size: int = 32
    learning_rate: float = 0.001
    num_epochs: int = 50
    weight_decay: float = 1e-4
    scheduler_step_size: int = 7
    scheduler_gamma: float = 0.1
    
    # Data parameters
    image_size: int = 224
    num_workers: int = 4
    train_split: float = 0.8
    val_split: float = 0.1
    test_split: float = 0.1
    
    # Augmentation parameters
    use_augmentation: bool = True
    rotation_degrees: int = 15
    horizontal_flip_prob: float = 0.5
    vertical_flip_prob: float = 0.0
    brightness_contrast: float = 0.2
    hue_saturation: float = 0.1
    
    # Paths
    data_dir: str = "data"
    models_dir: str = "models"
    logs_dir: str = "logs"
    
    # Macro estimation parameters
    macro_estimation_enabled: bool = True
    serving_size_estimation: bool = True
    
    # Food categories with macro information
    food_categories: Dict[str, Dict[str, float]] = {
        "apple_pie": {"calories": 237, "protein": 2.4, "carbs": 34.0, "fat": 11.0, "fiber": 1.8},
        "baby_back_ribs": {"calories": 290, "protein": 25.0, "carbs": 0.0, "fat": 20.0, "fiber": 0.0},
        "baklava": {"calories": 334, "protein": 4.0, "carbs": 45.0, "fat": 16.0, "fiber": 1.5},
        "beef_carpaccio": {"calories": 120, "protein": 20.0, "carbs": 0.0, "fat": 4.0, "fiber": 0.0},
        "beef_tartare": {"calories": 180, "protein": 25.0, "carbs": 2.0, "fat": 8.0, "fiber": 0.0},
        "beet_salad": {"calories": 43, "protein": 1.6, "carbs": 9.6, "fat": 0.2, "fiber": 2.8},
        "beignets": {"calories": 302, "protein": 4.0, "carbs": 35.0, "fat": 16.0, "fiber": 1.0},
        "bibimbap": {"calories": 320, "protein": 12.0, "carbs": 45.0, "fat": 12.0, "fiber": 6.0},
        "bread_pudding": {"calories": 245, "protein": 6.0, "carbs": 35.0, "fat": 10.0, "fiber": 1.5},
        "breakfast_burrito": {"calories": 350, "protein": 18.0, "carbs": 30.0, "fat": 18.0, "fiber": 3.0},
        "bruschetta": {"calories": 120, "protein": 4.0, "carbs": 15.0, "fat": 6.0, "fiber": 2.0},
        "caesar_salad": {"calories": 180, "protein": 8.0, "carbs": 8.0, "fat": 14.0, "fiber": 3.0},
        "cannoli": {"calories": 280, "protein": 6.0, "carbs": 35.0, "fat": 14.0, "fiber": 1.0},
        "caprese_salad": {"calories": 120, "protein": 6.0, "carbs": 8.0, "fat": 8.0, "fiber": 2.0},
        "carrot_cake": {"calories": 320, "protein": 5.0, "carbs": 45.0, "fat": 14.0, "fiber": 2.0},
        "ceviche": {"calories": 140, "protein": 20.0, "carbs": 8.0, "fat": 4.0, "fiber": 1.0},
        "cheesecake": {"calories": 350, "protein": 6.0, "carbs": 30.0, "fat": 22.0, "fiber": 0.5},
        "chicken_curry": {"calories": 280, "protein": 20.0, "carbs": 25.0, "fat": 12.0, "fiber": 4.0},
        "chicken_quesadilla": {"calories": 320, "protein": 18.0, "carbs": 25.0, "fat": 18.0, "fiber": 2.0},
        "chicken_wings": {"calories": 290, "protein": 25.0, "carbs": 0.0, "fat": 20.0, "fiber": 0.0},
        "chocolate_cake": {"calories": 380, "protein": 5.0, "carbs": 50.0, "fat": 18.0, "fiber": 2.0},
        "chocolate_mousse": {"calories": 280, "protein": 4.0, "carbs": 25.0, "fat": 18.0, "fiber": 1.0},
        "churros": {"calories": 320, "protein": 4.0, "carbs": 45.0, "fat": 14.0, "fiber": 1.0},
        "clam_chowder": {"calories": 180, "protein": 12.0, "carbs": 15.0, "fat": 8.0, "fiber": 2.0},
        "club_sandwich": {"calories": 350, "protein": 20.0, "carbs": 25.0, "fat": 18.0, "fiber": 2.0},
        "crab_cakes": {"calories": 220, "protein": 18.0, "carbs": 8.0, "fat": 12.0, "fiber": 1.0},
        "creme_brulee": {"calories": 320, "protein": 4.0, "carbs": 30.0, "fat": 20.0, "fiber": 0.0},
        "croque_madame": {"calories": 380, "protein": 18.0, "carbs": 25.0, "fat": 22.0, "fiber": 1.0},
        "cup_cakes": {"calories": 280, "protein": 4.0, "carbs": 40.0, "fat": 12.0, "fiber": 1.0},
        "deviled_eggs": {"calories": 140, "protein": 8.0, "carbs": 2.0, "fat": 12.0, "fiber": 0.0},
        "donuts": {"calories": 300, "protein": 4.0, "carbs": 45.0, "fat": 12.0, "fiber": 1.0},
        "dumplings": {"calories": 220, "protein": 8.0, "carbs": 35.0, "fat": 6.0, "fiber": 2.0},
        "edamame": {"calories": 120, "protein": 12.0, "carbs": 10.0, "fat": 5.0, "fiber": 5.0},
        "eggs_benedict": {"calories": 320, "protein": 16.0, "carbs": 8.0, "fat": 25.0, "fiber": 1.0},
        "escargots": {"calories": 140, "protein": 12.0, "carbs": 4.0, "fat": 8.0, "fiber": 1.0},
        "falafel": {"calories": 240, "protein": 8.0, "carbs": 30.0, "fat": 12.0, "fiber": 6.0},
        "filet_mignon": {"calories": 250, "protein": 25.0, "carbs": 0.0, "fat": 15.0, "fiber": 0.0},
        "fish_and_chips": {"calories": 380, "protein": 15.0, "carbs": 35.0, "fat": 20.0, "fiber": 2.0},
        "foie_gras": {"calories": 460, "protein": 8.0, "carbs": 2.0, "fat": 45.0, "fiber": 0.0},
        "french_fries": {"calories": 365, "protein": 4.0, "carbs": 63.0, "fat": 14.0, "fiber": 4.0},
        "french_onion_soup": {"calories": 180, "protein": 8.0, "carbs": 20.0, "fat": 8.0, "fiber": 2.0},
        "french_toast": {"calories": 280, "protein": 8.0, "carbs": 35.0, "fat": 12.0, "fiber": 1.0},
        "fried_calamari": {"calories": 260, "protein": 12.0, "carbs": 20.0, "fat": 14.0, "fiber": 1.0},
        "fried_rice": {"calories": 280, "protein": 8.0, "carbs": 45.0, "fat": 8.0, "fiber": 2.0},
        "frozen_yogurt": {"calories": 140, "protein": 4.0, "carbs": 25.0, "fat": 4.0, "fiber": 0.0},
        "garlic_bread": {"calories": 280, "protein": 8.0, "carbs": 40.0, "fat": 12.0, "fiber": 2.0},
        "gnocchi": {"calories": 220, "protein": 6.0, "carbs": 40.0, "fat": 4.0, "fiber": 2.0},
        "greek_salad": {"calories": 160, "protein": 6.0, "carbs": 8.0, "fat": 12.0, "fiber": 3.0},
        "grilled_cheese_sandwich": {"calories": 320, "protein": 12.0, "carbs": 25.0, "fat": 18.0, "fiber": 1.0},
        "grilled_salmon": {"calories": 280, "protein": 30.0, "carbs": 0.0, "fat": 16.0, "fiber": 0.0},
        "guacamole": {"calories": 160, "protein": 2.0, "carbs": 8.0, "fat": 14.0, "fiber": 4.0},
        "hamburger": {"calories": 350, "protein": 20.0, "carbs": 25.0, "fat": 18.0, "fiber": 2.0},
        "hot_and_sour_soup": {"calories": 120, "protein": 8.0, "carbs": 15.0, "fat": 4.0, "fiber": 2.0},
        "hot_dog": {"calories": 280, "protein": 12.0, "carbs": 20.0, "fat": 18.0, "fiber": 1.0},
        "huevos_rancheros": {"calories": 320, "protein": 16.0, "carbs": 25.0, "fat": 18.0, "fiber": 4.0},
        "hummus": {"calories": 160, "protein": 6.0, "carbs": 15.0, "fat": 8.0, "fiber": 4.0},
        "ice_cream": {"calories": 200, "protein": 4.0, "carbs": 25.0, "fat": 10.0, "fiber": 0.0},
        "lasagna": {"calories": 320, "protein": 18.0, "carbs": 25.0, "fat": 18.0, "fiber": 3.0},
        "lobster_bisque": {"calories": 220, "protein": 12.0, "carbs": 15.0, "fat": 12.0, "fiber": 1.0},
        "lobster_roll_sandwich": {"calories": 320, "protein": 16.0, "carbs": 25.0, "fat": 18.0, "fiber": 1.0},
        "macaroni_and_cheese": {"calories": 320, "protein": 12.0, "carbs": 35.0, "fat": 14.0, "fiber": 2.0},
        "macarons": {"calories": 90, "protein": 2.0, "carbs": 12.0, "fat": 4.0, "fiber": 0.0},
        "miso_soup": {"calories": 60, "protein": 4.0, "carbs": 8.0, "fat": 2.0, "fiber": 1.0},
        "mussels": {"calories": 140, "protein": 18.0, "carbs": 4.0, "fat": 6.0, "fiber": 0.0},
        "nachos": {"calories": 380, "protein": 12.0, "carbs": 35.0, "fat": 22.0, "fiber": 3.0},
        "omelette": {"calories": 220, "protein": 14.0, "carbs": 4.0, "fat": 16.0, "fiber": 1.0},
        "onion_rings": {"calories": 320, "protein": 4.0, "carbs": 35.0, "fat": 18.0, "fiber": 2.0},
        "oysters": {"calories": 80, "protein": 8.0, "carbs": 4.0, "fat": 4.0, "fiber": 0.0},
        "pad_thai": {"calories": 320, "protein": 12.0, "carbs": 45.0, "fat": 12.0, "fiber": 3.0},
        "paella": {"calories": 280, "protein": 16.0, "carbs": 35.0, "fat": 10.0, "fiber": 3.0},
        "pancakes": {"calories": 220, "protein": 6.0, "carbs": 35.0, "fat": 8.0, "fiber": 1.0},
        "panna_cotta": {"calories": 280, "protein": 4.0, "carbs": 25.0, "fat": 18.0, "fiber": 0.0},
        "peking_duck": {"calories": 320, "protein": 25.0, "carbs": 8.0, "fat": 20.0, "fiber": 1.0},
        "pho": {"calories": 220, "protein": 16.0, "carbs": 25.0, "fat": 8.0, "fiber": 2.0},
        "pizza": {"calories": 280, "protein": 12.0, "carbs": 35.0, "fat": 12.0, "fiber": 2.0},
        "pork_chop": {"calories": 280, "protein": 25.0, "carbs": 0.0, "fat": 18.0, "fiber": 0.0},
        "poutine": {"calories": 420, "protein": 12.0, "carbs": 35.0, "fat": 25.0, "fiber": 2.0},
        "prime_rib": {"calories": 320, "protein": 28.0, "carbs": 0.0, "fat": 22.0, "fiber": 0.0},
        "pulled_pork_sandwich": {"calories": 350, "protein": 20.0, "carbs": 25.0, "fat": 18.0, "fiber": 2.0},
        "ramen": {"calories": 280, "protein": 12.0, "carbs": 35.0, "fat": 12.0, "fiber": 2.0},
        "ravioli": {"calories": 240, "protein": 10.0, "carbs": 35.0, "fat": 8.0, "fiber": 2.0},
        "red_velvet_cake": {"calories": 350, "protein": 5.0, "carbs": 45.0, "fat": 16.0, "fiber": 1.0},
        "risotto": {"calories": 280, "protein": 8.0, "carbs": 45.0, "fat": 8.0, "fiber": 2.0},
        "samosa": {"calories": 260, "protein": 6.0, "carbs": 30.0, "fat": 14.0, "fiber": 3.0},
        "sashimi": {"calories": 120, "protein": 20.0, "carbs": 0.0, "fat": 4.0, "fiber": 0.0},
        "scallops": {"calories": 140, "protein": 20.0, "carbs": 4.0, "fat": 6.0, "fiber": 0.0},
        "seaweed_salad": {"calories": 60, "protein": 4.0, "carbs": 8.0, "fat": 2.0, "fiber": 2.0},
        "shrimp_and_grits": {"calories": 280, "protein": 16.0, "carbs": 25.0, "fat": 14.0, "fiber": 2.0},
        "spaghetti_bolognese": {"calories": 320, "protein": 16.0, "carbs": 35.0, "fat": 12.0, "fiber": 3.0},
        "spaghetti_carbonara": {"calories": 380, "protein": 16.0, "carbs": 35.0, "fat": 18.0, "fiber": 2.0},
        "spring_rolls": {"calories": 180, "protein": 6.0, "carbs": 25.0, "fat": 8.0, "fiber": 3.0},
        "steak": {"calories": 280, "protein": 25.0, "carbs": 0.0, "fat": 18.0, "fiber": 0.0},
        "strawberry_shortcake": {"calories": 280, "protein": 4.0, "carbs": 35.0, "fat": 14.0, "fiber": 1.0},
        "sushi": {"calories": 140, "protein": 8.0, "carbs": 20.0, "fat": 4.0, "fiber": 1.0},
        "tacos": {"calories": 220, "protein": 12.0, "carbs": 20.0, "fat": 12.0, "fiber": 3.0},
        "takoyaki": {"calories": 180, "protein": 8.0, "carbs": 20.0, "fat": 8.0, "fiber": 1.0},
        "tiramisu": {"calories": 320, "protein": 6.0, "carbs": 35.0, "fat": 16.0, "fiber": 1.0},
        "tuna_tartare": {"calories": 160, "protein": 20.0, "carbs": 4.0, "fat": 8.0, "fiber": 1.0},
        "waffles": {"calories": 260, "protein": 6.0, "carbs": 35.0, "fat": 12.0, "fiber": 1.0}
    }
    
    def __post_init__(self):
        """Create directories if they don't exist"""
        for dir_path in [self.data_dir, self.models_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)

# Global configuration instance
config = ModelConfig() 