# rename_folders.py
from pathlib import Path
import shutil
import json

# Load mapping
with open('include50_mapping_complete.json', 'r') as f:
    sign_mapping = json.load(f)

print("🔄 Renaming folders to clean sign names")
print("="*70)

lstm_path = Path("lstm_data")

# Get all folders
folders = [f for f in lstm_path.iterdir() if f.is_dir()]
print(f"📁 Found {len(folders)} folders")

renamed = 0
unmatched = []

for folder in folders:
    folder_name = folder.name
    
    if folder_name in sign_mapping:
        new_name = sign_mapping[folder_name]
        new_path = lstm_path / new_name
        
        if new_path.exists():
            print(f"⚠️ {folder_name} -> {new_name} (merging)")
            # Merge files
            for file in folder.glob("*.npy"):
                shutil.move(str(file), str(new_path / file.name))
            folder.rmdir()
        else:
            print(f"✅ {folder_name} -> {new_name}")
            folder.rename(new_path)
        renamed += 1
    else:
        unmatched.append(folder_name)

print("="*70)
print(f"✅ Renamed: {renamed} folders")
print(f"❌ Unmatched: {len(unmatched)} folders")

if unmatched:
    print("\n❌ Unmatched folders:")
    for f in unmatched[:10]:
        print(f"   - {f}")