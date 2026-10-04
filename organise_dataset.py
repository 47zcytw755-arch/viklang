# organize_dataset_fixed.py
from pathlib import Path
import json
import shutil

print("📊 Organizing Dataset")
print("="*70)

# Load INCLUDE-50 mapping
with open('include50_mapping_complete.json', 'r') as f:
    include50_mapping = json.load(f)

# Get all clean INCLUDE-50 sign names
include50_signs = set(include50_mapping.values())

lstm_path = Path("lstm_data")

# Get all folders
folders = [f for f in lstm_path.iterdir() if f.is_dir()]

print(f"📁 Total folders: {len(folders)}")

# Categorize
include50_folders = []
extra_folders = []

for folder in folders:
    if folder.name in include50_signs:
        include50_folders.append(folder.name)
    else:
        extra_folders.append(folder.name)

print(f"\n[OK] INCLUDE-50 signs: {len(include50_folders)}")
print(f"[+] Extra signs: {len(extra_folders)}")

# Show extra signs
if extra_folders:
    print("\n📋 Extra signs (not in INCLUDE-50):")
    for sign in sorted(extra_folders):
        count = len(list((lstm_path / sign).glob("*.npy")))
        print(f"   - {sign}: {count} sequences")

# Create a summary file without emojis
with open('dataset_summary_complete.txt', 'w', encoding='utf-8') as f:
    f.write("COMPLETE DATASET SUMMARY\n")
    f.write("="*70 + "\n")
    f.write(f"Total signs: {len(folders)}\n")
    f.write(f"INCLUDE-50 signs: {len(include50_folders)}\n")
    f.write(f"Additional signs: {len(extra_folders)}\n\n")
    
    f.write("INCLUDE-50 Signs:\n")
    for sign in sorted(include50_folders):
        count = len(list((lstm_path / sign).glob("*.npy")))
        f.write(f"  [OK] {sign}: {count} sequences\n")
    
    if extra_folders:
        f.write("\nAdditional Signs:\n")
        for sign in sorted(extra_folders):
            count = len(list((lstm_path / sign).glob("*.npy")))
            f.write(f"  [+] {sign}: {count} sequences\n")

print(f"\n[OK] Summary saved to dataset_summary_complete.txt")