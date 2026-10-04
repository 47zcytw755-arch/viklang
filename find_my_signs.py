import requests
import zipfile
import os
from pathlib import Path
import json
import tempfile
import shutil

def explore_dataset_structure():
    """
    Explore what's inside the zip files without downloading everything
    """
    record_id = "4010759"
    base_url = f"https://zenodo.org/api/records/{record_id}"
    
    print("📡 Fetching file list...")
    response = requests.get(base_url)
    data = response.json()
    
    # Download just one zip file to explore
    zip_files = [f for f in data['files'] if f['key'].endswith('.zip')]
    
    print(f"\n📋 Found {len(zip_files)} zip files")
    print("\nCategories available:")
    
    categories = []
    for file_info in zip_files[:10]:  # Check first 10
        filename = file_info['key']
        # Extract category name (e.g., "Greetings_1of2.zip" -> "Greetings")
        category = filename.split('_')[0]
        if category not in categories:
            categories.append(category)
            print(f"  - {category}")
    
    return data

def download_and_extract_specific_categories():
    """
    Download only the categories that might contain your signs
    """
    record_id = "4010759"
    base_url = f"https://zenodo.org/api/records/{record_id}"
    
    print("📡 Fetching file list...")
    response = requests.get(base_url)
    data = response.json()
    
    # Categories you need
    needed_categories = [
        "Greetings",  # Contains "thank_you", "namaste", "yes"
        "Home",       # Contains "toilet", "food"
        "Society",    # Might contain "food"
        "People"      # Might contain "yes", "namaste"
    ]
    
    # Download zip files for these categories
    output_dir = Path("INCLUDE-50")
    output_dir.mkdir(exist_ok=True)
    
    downloaded_files = []
    
    for file_info in data['files']:
        filename = file_info['key']
        
        # Check if this file belongs to our needed categories
        for category in needed_categories:
            if filename.startswith(category):
                file_url = file_info['links']['self']
                file_size = file_info.get('size', 0)
                
                print(f"\n⬇️ Downloading: {filename} ({file_size/1024/1024:.1f} MB)")
                
                try:
                    file_response = requests.get(file_url, stream=True)
                    if file_response.status_code == 200:
                        file_path = output_dir / filename
                        
                        # Download with progress
                        with open(file_path, 'wb') as f:
                            for chunk in file_response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        print(f"   ✅ Downloaded")
                        downloaded_files.append(file_path)
                        
                        # Extract zip
                        print(f"   📦 Extracting...")
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(output_dir)
                        print(f"   ✅ Extracted")
                        
                    else:
                        print(f"   ❌ Failed to download")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
                
                break  # Found this file, move to next
    
    return downloaded_files

def find_your_signs():
    """
    Search for specific signs in the extracted files
    """
    include_path = Path("INCLUDE-50")
    
    signs_to_find = ["thank", "yes", "toilet", "food", "namaste"]
    
    print("\n🔍 Searching for your signs...")
    print("-" * 50)
    
    found_signs = {}
    
    # Search in all subdirectories
    for sign in signs_to_find:
        found_files = []
        for file_path in include_path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
                # Check if filename contains the sign
                if sign.lower() in file_path.name.lower():
                    found_files.append(file_path)
                # Also check parent folder name
                elif sign.lower() in str(file_path.parent).lower():
                    found_files.append(file_path)
        
        if found_files:
            found_signs[sign] = found_files
            print(f"\n✅ Found '{sign}':")
            for f in found_files[:5]:  # Show first 5
                print(f"   - {f.relative_to(include_path)}")
            if len(found_files) > 5:
                print(f"   ... and {len(found_files) - 5} more")
        else:
            print(f"\n❌ No files found for '{sign}'")
    
    return found_signs

def list_all_signs_in_dataset():
    """
    List all signs available in the dataset
    """
    include_path = Path("INCLUDE-50")
    
    if not include_path.exists():
        print("❌ INCLUDE-50 folder doesn't exist yet")
        return
    
    print("\n📋 All signs found in dataset:")
    print("-" * 50)
    
    all_signs = {}
    
    # Walk through all directories
    for folder in include_path.iterdir():
        if folder.is_dir():
            # Check if this folder contains video files
            video_files = list(folder.rglob("*.mp4")) + list(folder.rglob("*.avi"))
            if video_files:
                # Extract sign name from folder
                sign_name = folder.name.replace("_", " ")
                # Clean up the name
                sign_name = ' '.join(word for word in sign_name.split() if not word.isdigit())
                sign_name = sign_name.replace("of", "").strip()
                
                all_signs[sign_name] = len(video_files)
    
    # Sort and display
    for sign, count in sorted(all_signs.items())[:30]:
        print(f"   {sign}: {count} videos")

if __name__ == "__main__":
    print("="*60)
    print("INCLUDE-50 Sign Finder")
    print("="*60)
    
    # First, explore what's available
    data = explore_dataset_structure()
    
    # Download needed categories
    print("\n📥 Downloading relevant categories...")
    downloaded = download_and_extract_specific_categories()
    
    if downloaded:
        print(f"\n✅ Downloaded {len(downloaded)} zip files")
        
        # Search for your signs
        found = find_your_signs()
        
        # List all available signs
        list_all_signs_in_dataset()
        
        if found:
            print("\n" + "="*60)
            print("✅ Your signs have been downloaded!")
            print("="*60)
            for sign, files in found.items():
                print(f"\n📁 {sign}: {len(files)} video files")
        else:
            print("\n⚠️ Couldn't find your specific signs.")
            print("\nLet's check what's actually available:")
            
            # Show all categories
            include_path = Path("INCLUDE-50")
            if include_path.exists():
                print("\nAvailable folders:")
                for folder in include_path.iterdir():
                    if folder.is_dir():
                        videos = list(folder.rglob("*.mp4")) + list(folder.rglob("*.avi"))
                        if videos:
                            print(f"   - {folder.name}: {len(videos)} videos")
    else:
        print("\n❌ No files downloaded. Checking alternative...")
        print("\n🔍 Looking for INCLUDE-50 on HuggingFace...")
        
        try:
            from datasets import load_dataset
            
            dataset = load_dataset("ai4bharat/INCLUDE", split="train", streaming=True)
            
            # Get all signs with include_50 = True
            include_50_signs = []
            for i, item in enumerate(dataset):
                if i > 1000:  # Limit to avoid too much processing
                    break
                if item.get('include_50', False):
                    include_50_signs.append(item.get('label', ''))
            
            print(f"\n📋 Found {len(set(include_50_signs))} INCLUDE-50 signs")
            
        except Exception as e:
            print(f"   Error: {e}")