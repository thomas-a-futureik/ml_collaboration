"""
Data splitting utility for creating train/validation/test datasets.

This script takes raw image data and splits it into training, validation,
and test sets while maintaining class distributions.
"""
import os
import glob
import random
import shutil
import logging
from pathlib import Path
from tqdm import tqdm

# Import configuration
from config import (
    RAW_IMAGES_DIR, PROCESSED_IMAGES_DIR, SPLIT_SEED,
    TRAIN_RATIO, VAL_RATIO, TEST_RATIO, LOG_LEVEL, LOG_FILE,
    calculate_splits, TASKS, TASK_DIRS
)

# Set up logging
os.makedirs(LOG_FILE.parent, exist_ok=True)
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def copy_files(file_paths, destination):
    """Copy files to destination directory."""
    os.makedirs(destination, exist_ok=True)
    for src in tqdm(file_paths, desc=f"Copying to {destination.name}"):
        try:
            shutil.copy2(src, destination)
        except Exception as e:
            logger.error(f"Error copying {src}: {e}")

def get_task_label(image_path, task):
    """Extract task-specific label from image path or metadata.
    
    Args:
        image_path: Path to the image file
        task: Task name ('age', 'gender', 'expression', 'race')
        
    Returns:
        Label for the specified task
    """
    # This is a placeholder implementation
    # You'll need to implement the actual logic to extract the label
    # based on your file naming convention or metadata
    
    # Example: If your files are named like 'age_25_gender_male_expression_happy.jpg'
    # You could parse the filename to get the labels
    filename = os.path.basename(image_path).lower()
    
    # Default fallback
    if task == 'age':
        return '20-29'  # Default age group
    elif task == 'gender':
        return 'male' if 'male' in filename else 'female'
    elif task == 'expression':
        # Check for any expression in filename
        for expr in TASKS['expression']['classes']:
            if expr in filename:
                return expr
        return 'neutral'  # Default expression
    elif task == 'race':
        # Check for any race in filename
        for race in TASKS['race']['classes']:
            if race in filename:
                return race
        return 'others'  # Default race
    
    return 'unknown'

def split_dataset():
    """Split dataset into train/validation/test sets for all tasks."""
    logger.info("Starting dataset splitting process")
    
    # Set random seed for reproducibility
    random.seed(SPLIT_SEED)
    
    # Get all image files
    pattern = os.path.join(RAW_IMAGES_DIR, '**/*.jpg')
    all_files = glob.glob(pattern, recursive=True)
    
    if not all_files:
        logger.error(f"No JPG files found in {RAW_IMAGES_DIR}")
        return
    
    logger.info(f"Found {len(all_files)} total images")
    
    # Shuffle all files
    random.shuffle(all_files)
    
    # Calculate split sizes
    n_total = len(all_files)
    n_train, n_val, n_test = calculate_splits(n_total)
    
    # Split the files
    train_files = all_files[:n_train]
    val_files = all_files[n_train:n_train + n_val]
    test_files = all_files[n_train + n_val:]
    
    logger.info(f"Split sizes - Train: {len(train_files)}, Val: {len(val_files)}, Test: {len(test_files)}")
    
    # Process each task
    for task, task_info in TASKS.items():
        logger.info(f"\nProcessing task: {task.upper()}")
        
        # Process each split
        for split_name, files in [('train', train_files), ('val', val_files), ('test', test_files)]:
            logger.info(f"  Processing {split_name} split")
            
            for src_path in tqdm(files, desc=f"{task} - {split_name}"):
                try:
                    # Get task-specific label for this image
                    label = get_task_label(src_path, task)
                    
                    # Skip if label is not in our defined classes
                    if label not in task_info['classes']:
                        logger.warning(f"Skipping image with unknown {task} label: {src_path}")
                        continue
                    
                    # Determine destination path
                    dest_dir = TASK_DIRS[task][split_name] / label
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    # Copy the file
                    shutil.copy2(src_path, dest_dir)
                    
                except Exception as e:
                    logger.error(f"Error processing {src_path}: {e}")
    
    logger.info("Dataset splitting completed successfully")
    
    logger.info("Dataset splitting completed successfully")

if __name__ == "__main__":
    try:
        logger.info("=" * 70)
        logger.info("Starting data split process")
        logger.info(f"Source directory: {RAW_IMAGES_DIR}")
        logger.info(f"Destination directory: {PROCESSED_IMAGES_DIR}")
        logger.info(f"Split ratios - Train: {TRAIN_RATIO}, Val: {VAL_RATIO}, Test: {TEST_RATIO}")
        
        # Log tasks and their classes
        logger.info("\nTasks and their classes:")
        for task, info in TASKS.items():
            logger.info(f"  {task.upper()}: {', '.join(info['classes'])}")
        
        logger.info("\n" + "-" * 70)
        
        split_dataset()
        
        logger.info("\n" + "=" * 70)
        logger.info("Data split completed successfully")
        logger.info("=" * 70)
    except Exception as e:
        logger.error(f"Error during data splitting: {e}", exc_info=True)
        raise