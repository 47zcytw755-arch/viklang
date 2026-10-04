from datasets import load_dataset
from collections import Counter

print("📡 Loading INCLUDE dataset...")
dataset = load_dataset("ai4bharat/INCLUDE", split="train")

# Get all signs with include_50 = True
include_50_signs = []
for item in dataset:
    if item.get('include_50', False):
        include_50_signs.append(item.get('label', ''))

# Count and sort
sign_counts = Counter(include_50_signs)
unique_signs = sorted(sign_counts.keys())

print(f"\n✅ Found {len(unique_signs)} INCLUDE-50 signs:")
print("="*50)

# Display all signs with their numbers
for i, sign in enumerate(unique_signs, 1):
    print(f"{i:3d}. {sign}")

print("\n" + "="*50)
print("🔍 Searching for your specific signs:")
print("-"*50)

# Your signs to find
your_signs = ["thank", "yes", "toilet", "food", "namaste", "no", "please", "hello"]

for search_term in your_signs:
    found = []
    for sign in unique_signs:
        if search_term.lower() in sign.lower():
            found.append(sign)
    
    if found:
        print(f"✅ '{search_term}' found as:")
        for f in found:
            print(f"   - {f} (count: {sign_counts[f]})")
    else:
        print(f"❌ '{search_term}' not found")
        # Suggest similar signs
        similar = [s for s in unique_signs if any(word in s.lower() for word in search_term.split())]
        if similar:
            print(f"   Did you mean: {', '.join(similar[:3])}")

# Also check which signs you already have in your folder
print("\n" + "="*50)
print("📂 Checking your local files:")
print("-"*50)

import os
from pathlib import Path

include_path = Path("INCLUDE-50")
if include_path.exists():
    # Check what zip files you have
    zip_files = list(include_path.glob("*.zip"))
    if zip_files:
        print(f"Found {len(zip_files)} zip files:")
        for zf in zip_files:
            size = zf.stat().st_size / 1024 / 1024
            print(f"   - {zf.name} ({size:.1f} MB)")
    
    # Check extracted folders
    folders = [f for f in include_path.iterdir() if f.is_dir()]
    if folders:
        print(f"\nFound {len(folders)} extracted folders:")
        for folder in folders:
            videos = list(folder.rglob("*.mp4")) + list(folder.rglob("*.avi"))
            print(f"   - {folder.name}: {len(videos)} videos")
else:
    print("INCLUDE-50 folder not found")