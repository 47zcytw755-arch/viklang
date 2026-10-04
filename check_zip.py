import zipfile
from pathlib import Path
import os

zip_path = Path("INCLUDE-50/Home_4of4.zip")

if zip_path.exists():
    print(f"📦 Checking contents of {zip_path.name}")
    print("="*50)
    
    # List contents without extracting
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        
        print(f"Total files in zip: {len(file_list)}")
        
        # Show first 20 files
        print("\nFirst 20 files:")
        for f in file_list[:20]:
            print(f"  - {f}")
        
        # Search for your signs
        signs_to_find = ["toilet", "food", "eat", "drink", "bathroom"]
        
        print("\n" + "="*50)
        print("🔍 Searching for your signs:")
        
        for sign in signs_to_find:
            found = [f for f in file_list if sign.lower() in f.lower()]
            if found:
                print(f"\n✅ '{sign}' found:")
                for f in found[:5]:
                    print(f"   - {f}")
            else:
                print(f"\n❌ '{sign}' not found")
        
        # Extract only the files we need
        print("\n" + "="*50)
        print("📂 Extracting...")
        
        # Extract all
        extract_path = Path("INCLUDE-50/Home")
        extract_path.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        print(f"✅ Extracted to: {extract_path}")
        
        # Count videos
        video_files = list(extract_path.rglob("*.mp4")) + list(extract_path.rglob("*.avi"))
        print(f"📹 Found {len(video_files)} video files")
else:
    print("❌ Home_4of4.zip not found")
    print("Current directory contents:")
    for f in Path("INCLUDE-50").iterdir():
        print(f"  - {f.name}")