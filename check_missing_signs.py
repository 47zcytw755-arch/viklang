# check_missing_signs.py
from pathlib import Path

# Get all INCLUDE-50 sign names from your folders
include_path = Path("INCLUDE-50-ALL")
lstm_path = Path("lstm_data")

print("📊 Comparing INCLUDE-50 vs Your Dataset")
print("="*70)

# Get all folders with videos from INCLUDE-50
include_folders = []
for folder in include_path.iterdir():
    if folder.is_dir():
        videos = list(folder.rglob('*.mp4')) + list(folder.rglob('*.avi'))
        if videos:
            include_folders.append(folder.name)

print(f"📂 INCLUDE-50 folders with videos: {len(include_folders)}")

# Get signs already converted
converted_signs = []
for folder in lstm_path.iterdir():
    if folder.is_dir():
        npy_files = list(folder.glob("*.npy"))
        if npy_files:
            converted_signs.append(folder.name)

print(f"✅ Already converted: {len(converted_signs)} signs")
print(f"❌ Missing: {len(include_folders) - len(converted_signs)} signs")

# Show missing signs
missing = set(include_folders) - set(converted_signs)
if missing:
    print("\n❌ Missing signs:")
    for sign in sorted(missing):
        print(f"   - {sign}")
else:
    print("\n🎉 All signs converted!")