import os
from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
RAW_IMAGES_DIR = DATA_DIR / 'raw'  # Source of original images
PROCESSED_DIR = DATA_DIR / 'processed'  # Where processed images will go

# Data split ratios (must sum to 1.0)
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Random seed for reproducibility
SEED = 42

# Image settings
IMAGE_SIZE = (224, 224)  # (height, width)

# Class mapping (directory name -> label name)
CLASS_MAPPING = {
    '0': 'female',
    '1': 'male'
}

def get_split_sizes(total_samples):
    """Calculate number of samples for each split."""
    n_train = int(total_samples * TRAIN_RATIO)
    n_val = int(total_samples * VAL_RATIO)
    n_test = total_samples - n_train - n_val
    return n_train, n_val, n_test

def setup_directories():
    """Create necessary directories if they don't exist."""
    # Create main directories
    os.makedirs(RAW_IMAGES_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Create train/val/test directories for each class
    for split in ['train', 'val', 'test']:
        split_dir = PROCESSED_DIR / split
        for class_name in CLASS_MAPPING.values():
            os.makedirs(split_dir / class_name, exist_ok=True)

# Setup directories when this module is imported
setup_directories()