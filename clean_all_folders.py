# clean_all_folders.py
from pathlib import Path
import re
import shutil

print("🧹 Cleaning ALL folder names")
print("="*70)

lstm_path = Path("lstm_data")

# Get all folders
folders = [f for f in lstm_path.iterdir() if f.is_dir()]
print(f"📁 Found {len(folders)} folders")

# Function to clean folder name
def clean_folder_name(name):
    # Remove numbers at start (e.g., "1. religion" -> "religion")
    cleaned = re.sub(r'^\d+\.\s*', '', name)
    # Remove numbers in middle (e.g., "44. it" -> "it")
    cleaned = re.sub(r'^\d+\.\s*', '', cleaned)
    # Replace spaces and special chars with underscore
    cleaned = re.sub(r'[^\w\s]', '', cleaned)
    cleaned = cleaned.lower().strip()
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned

# Process each folder
renamed = 0
cleaned_names = {}

for folder in folders:
    old_name = folder.name
    new_name = clean_folder_name(old_name)
    
    if old_name != new_name:
        new_path = lstm_path / new_name
        
        # Check if target already exists
        if new_path.exists():
            print(f"⚠️ {old_name} -> {new_name} (merging)")
            # Merge files
            for file in folder.glob("*.npy"):
                shutil.move(str(file), str(new_path / file.name))
            folder.rmdir()
        else:
            print(f"✅ {old_name} -> {new_name}")
            folder.rename(new_path)
        renamed += 1
        cleaned_names[old_name] = new_name
    else:
        print(f"⏭️ {old_name} (already clean)")

print("="*70)
print(f"✅ Renamed: {renamed} folders")
print(f"⏭️ Already clean: {len(folders) - renamed} folders")

# Show final list
print("\n📁 Final folder list:")
for folder in sorted(lstm_path.iterdir()):
    if folder.is_dir():
        npy_files = list(folder.glob("*.npy"))
        if npy_files:
            print(f"   ✅ {folder.name}: {len(npy_files)} sequences")