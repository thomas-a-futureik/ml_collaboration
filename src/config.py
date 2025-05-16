"""
Configuration settings for the image classification project.
"""
from pathlib import Path
import os

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
RAW_IMAGES_DIR = DATA_DIR / 'raw'  # Keeping existing path for backward compatibility
PROCESSED_IMAGES_DIR = DATA_DIR / 'processed'  # Keeping existing path
MODELS_DIR = Path("models")  # Keeping existing path

# Data split configuration
SPLIT_SEED = 42  # For reproducibility
TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

# Maintain backward compatibility with existing N_TRAIN and N_TEST
# These will be calculated based on actual data if not specified
N_TRAIN = 2500  # Will be overridden if calculate_splits is called
N_TEST = 500    # Will be overridden if calculate_splits is called

# Image processing
IMAGE_SIZE = (224, 224)  # (height, width)
IMAGE_CHANNELS = 3  # RGB

# Class names - update this based on your dataset
CLASSES = ["class1", "class2"]  # Keeping existing classes

# Training parameters (used in model training scripts)
BATCH_SIZE = 32
NUM_EPOCHS = 50
LEARNING_RATE = 1e-4

# MLflow configuration
MLFLOW_TRACKING_URI = 'file:' + str(PROJECT_ROOT / 'mlruns')

# DVC configuration
DVC_REMOTE = 'origin'  # Change to your DVC remote name

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = PROJECT_ROOT / 'logs' / 'data_processing.log'

# Create necessary directories
for directory in [PROCESSED_IMAGES_DIR, MODELS_DIR, LOG_FILE.parent]:
    os.makedirs(directory, exist_ok=True)

# Task definitions
TASKS = {
    'age': {
        'classes': ['0-2', '3-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+'],
        'type': 'classification',
    },
    'gender': {
        'classes': ['male', 'female'],
        'type': 'classification',
    },
    'expression': {
        'classes': ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'],
        'type': 'classification',
    },
    'race': {
        'classes': ['white', 'black', 'asian', 'indian', 'others'],
        'type': 'classification',
    },
}

# Dataset split directories structure
TASK_DIRS = {}
for task in TASKS:
    TASK_DIRS[task] = {
        'train': PROCESSED_IMAGES_DIR / task / 'train',
        'val': PROCESSED_IMAGES_DIR / task / 'val',
        'test': PROCESSED_IMAGES_DIR / task / 'test',
    }

# For backward compatibility
TRAIN_DIR = PROCESSED_IMAGES_DIR / 'train'
VAL_DIR = PROCESSED_IMAGES_DIR / 'val'
TEST_DIR = PROCESSED_IMAGES_DIR / 'test'

def calculate_splits(total_samples):
    """Calculate train/val/test split counts based on ratios."""
    n_train = int(total_samples * TRAIN_RATIO)
    n_val = int(total_samples * VAL_RATIO)
    n_test = total_samples - n_train - n_val
    return n_train, n_val, n_test

def create_split_directories():
    """Create necessary directories for all task splits."""
    for task, dirs in TASK_DIRS.items():
        for split_dir in dirs.values():
            os.makedirs(split_dir, exist_ok=True)
            for class_name in TASKS[task]['classes']:
                os.makedirs(os.path.join(split_dir, class_name), exist_ok=True)
    
    # Create legacy directories for backward compatibility
    for split_dir in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
        os.makedirs(split_dir, exist_ok=True)
        if 'CLASSES' in globals():  # Only if CLASSES is defined
            for class_name in CLASSES:
                os.makedirs(os.path.join(split_dir, class_name), exist_ok=True)

# Initialize directories
create_split_directories()

# Add __all__ for clean imports
__all__ = [
    'PROJECT_ROOT', 'DATA_DIR', 'RAW_IMAGES_DIR', 'PROCESSED_IMAGES_DIR', 'MODELS_DIR',
    'SPLIT_SEED', 'TRAIN_RATIO', 'VAL_RATIO', 'TEST_RATIO', 'N_TRAIN', 'N_TEST',
    'IMAGE_SIZE', 'IMAGE_CHANNELS', 'CLASSES', 'BATCH_SIZE', 'NUM_EPOCHS',
    'LEARNING_RATE', 'MLFLOW_TRACKING_URI', 'DVC_REMOTE', 'LOG_LEVEL', 'LOG_FILE',
    'TRAIN_DIR', 'VAL_DIR', 'TEST_DIR', 'TASKS', 'TASK_DIRS',
    'calculate_splits', 'create_split_directories'
]