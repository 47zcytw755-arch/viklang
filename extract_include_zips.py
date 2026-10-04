import os
import shutil
from pathlib import Path
import zipfile
import glob

def find_and_extract_zips():
    """
    Find all INCLUDE zip files and extract them to the right location
    """
    print("="*60)
    print("📦 INCLUDE Zip Files Extractor")
    print("="*60)
    
    # Common locations where you might have downloaded
    search_locations = [
        Path.home() / "Downloads",
        Path.home() / "Desktop",
        Path("C:/Users/KIIT/Downloads"),
        Path("C:/Users/KIIT/Desktop"),
        Path("C:/Users/KIIT/My project (2)"),
    ]
    
    # Target directory
    target_dir = Path("INCLUDE-50-ALL")
    target_dir.mkdir(exist_ok=True)
    
    # Keywords to identify INCLUDE files
    include_keywords = [
        'greetings', 'home', 'society', 'people', 'adjectives',
        'days', 'colours', 'animals', 'jobs', 'pronouns',
        'include', 'places', 'electronics', 'clothes'
    ]
    
    found_zips = []
    
    print("\n🔍 Searching for zip files...")
    print("-"*50)
    
    for location in search_locations:
        if not location.exists():
            continue
            
        print(f"\n📂 Checking: {location}")
        
        # Find all zip files
        for zip_file in location.glob("*.zip"):
            zip_name = zip_file.name.lower()
            
            # Check if this is an INCLUDE file
            is_include = any(keyword in zip_name for keyword in include_keywords)
            
            if is_include:
                size_mb = zip_file.stat().st_size / 1024 / 1024
                print(f"   ✅ Found: {zip_file.name} ({size_mb:.1f} MB)")
                found_zips.append(zip_file)
    
    if not found_zips:
        print("\n❌ No INCLUDE zip files found!")
        print("\nPlease check:")
        print("1. Did you download them to Downloads folder?")
        print("2. Did you download them to Desktop?")
        print("3. What are the filenames? (They should start with 'Greetings', 'Home', etc.)")
        return
    
    print(f"\n✅ Found {len(found_zips)} zip files")
    print(f"📊 Total size: {sum(f.stat().st_size for f in found_zips)/1024/1024/1024:.1f} GB")
    
    # Ask for confirmation
    response = input("\n📦 Extract all files to INCLUDE-50-ALL? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return
    
    print("\n" + "="*60)
    print("📦 Extracting files...")
    print("="*60)
    
    for i, zip_file in enumerate(found_zips, 1):
        print(f"\n[{i}/{len(found_zips)}] 📦 {zip_file.name}")
        
        try:
            # Extract to target directory
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(target_dir)
            print(f"   ✅ Extracted successfully")
            
        except zipfile.BadZipFile:
            print(f"   ❌ Corrupted zip file!")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Check what was extracted
    print("\n" + "="*60)
    print("📊 Extraction Complete!")
    print("="*60)
    
    # Show what's in the target directory
    if target_dir.exists():
        print("\n📁 Extracted folders:")
        for folder in target_dir.iterdir():
            if folder.is_dir():
                videos = list(folder.rglob("*.mp4")) + list(folder.rglob("*.avi"))
                if videos:
                    print(f"   📁 {folder.name}: {len(videos)} videos")
                else:
                    # Check subfolders
                    sub_videos = []
                    for sub in folder.rglob("*"):
                        if sub.is_file() and sub.suffix.lower() in ['.mp4', '.avi']:
                            sub_videos.append(sub)
                    if sub_videos:
                        print(f"   📁 {folder.name}: {len(sub_videos)} videos in subfolders")
                    else:
                        print(f"   📁 {folder.name}: No videos found (check subfolders)")

if __name__ == "__main__":
    find_and_extract_zips()