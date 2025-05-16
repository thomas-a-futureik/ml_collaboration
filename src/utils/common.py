from pathlib import Path
import shutil
from tqdm import tqdm
import time

def _copy_directory_contents(src, dst):
    """Helper function to copy directory contents with progress and logging."""
    src = Path(src)
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)

    items = list(src.iterdir())  # list first for tqdm to know length
    start_time = time.time()

    success_count = 0
    error_count = 0

    print(f"\n🔄 Copying from:\n  {src}\n➡️ To:\n  {dst}\n")

    for item in tqdm(items, desc="Copying files"):
        dest = dst / item.name
        try:
            if item.is_dir():
                shutil.copytree(item, dest, dirs_exist_ok=True)
            else:
                shutil.copy2(item, dest)
            success_count += 1
        except Exception as e:
            print(f"❌ Error copying {item.name}: {e}")
            error_count += 1

    elapsed = time.time() - start_time

    print(f"\n✅ Copy complete: {success_count} succeeded, ❌ {error_count} failed.")
    print(f"⏱️ Time taken: {elapsed:.2f} seconds.\n")




def get_directory_size(directory_path, unit='MB', verbose=False):
    """
    Recursively computes the total size of all files in a directory.

    Args:
        directory_path (str or Path): Directory whose size needs to be calculated.
        unit (str): 'B', 'KB', 'MB', or 'GB'. Default is 'MB'.
        verbose (bool): If True, prints file-wise size logging.

    Returns:
        float: Total size in the specified unit.
    """
    path = Path(directory_path)

    if not path.exists() or not path.is_dir():
        raise ValueError(f"❌ Invalid directory: {directory_path}")

    total_bytes = 0
    for file in path.rglob('*'):
        if file.is_file():
            try:
                size = file.stat().st_size
                total_bytes += size
                if verbose:
                    print(f"🧾 {file} --> {round(size / 1024**2, 2)} MB")
            except Exception as e:
                if verbose:
                    print(f"⚠️ Could not access {file}: {e}")

    # Conversion
    unit = unit.upper()
    unit_map = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 ** 2,
        'GB': 1024 ** 3,
    }

    if unit not in unit_map:
        raise ValueError(f"❌ Unsupported unit: {unit}. Use 'B', 'KB', 'MB', or 'GB'.")

    converted_size = round(total_bytes / unit_map[unit], 2)
    print(f"\n📦 Total directory size: {converted_size} {unit}")
    return converted_size
