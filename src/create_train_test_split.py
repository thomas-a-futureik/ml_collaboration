import os
import random
import shutil
from pathlib import Path
from tqdm import tqdm
from config import (
    RAW_IMAGES_DIR, PROCESSED_DIR, SEED,
    TRAIN_RATIO, VAL_RATIO, CLASS_MAPPING, get_split_sizes
)

def get_images():
    """Get all images from the raw directory."""
    image_extensions = ('.jpg', '.jpeg', '.png')
    images = []
    
    for root, _, files in os.walk(RAW_IMAGES_DIR):
        for file in files:
            if file.lower().endswith(image_extensions):
                images.append(Path(root) / file)
    
    return images

def copy_images(images, split_name ,task_name="gender"):
    """Copy images to their respective split and class directories."""
    for img_path in tqdm(images, desc=f"Copying {split_name} images"):
        try:
            # Get class from parent directory name (e.g., '0' or '1')
            class_dir = img_path.parent.name
            if class_dir not in CLASS_MAPPING:
                print(f"Skipping unknown class: {class_dir}")
                continue
                
            # Get the human-readable class name
            class_name = CLASS_MAPPING[class_dir]
            
            # Create destination directory
            dest_dir = PROCESSED_DIR /task_name/split_name / class_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy the image
            shutil.copy2(img_path, dest_dir / img_path.name)
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")

def main():
    print("=" * 50)
    print("Starting data split process")
    print(f"Source: {RAW_IMAGES_DIR}")
    print(f"Destination: {PROCESSED_DIR}")
    print(f"Split ratios: Train={TRAIN_RATIO}, Val={VAL_RATIO}, Test={1-TRAIN_RATIO-VAL_RATIO:.2f}")
    print("-" * 50)
    
    # Set random seed for reproducibility
    random.seed(SEED)
    
    # Get all images
    all_images = get_images()
    print(f"Found {len(all_images)} images")
    
    # Shuffle the images
    random.shuffle(all_images)
    
    # Calculate split sizes
    n_train, n_val, _ = get_split_sizes(len(all_images))
    
    # Split the data
    train_images = all_images[:n_train]
    val_images = all_images[n_train:n_train + n_val]
    test_images = all_images[n_train + n_val:]
    
    print(f"Splitting into: {len(train_images)} train, {len(val_images)} val, {len(test_images)} test")
    
    # Copy images to their respective directories
    copy_images(train_images, 'train')
    copy_images(val_images, 'val')
    copy_images(test_images, 'test')
    
    print("\nData split completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()