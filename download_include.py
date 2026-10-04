import requests
import zipfile
import os
from pathlib import Path
import json

def download_include_dataset():
    """
    Download INCLUDE dataset from Zenodo
    """
    # Zenodo record ID for INCLUDE dataset
    record_id = "4010759"
    base_url = f"https://zenodo.org/api/records/{record_id}"
    
    print(f"📡 Fetching file list from: {base_url}")
    
    # Get file list
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"❌ Error: Could not fetch record (status: {response.status_code})")
        return
    
    data = response.json()
    
    if 'files' not in data:
        print("❌ No files found")
        return
    
    # Create output directory
    output_dir = Path("INCLUDE-50")
    output_dir.mkdir(exist_ok=True)
    
    # List of INCLUDE-50 signs you need
    needed_signs = [
        "thank_you", "thank you", "thanks",
        "yes", 
        "toilet", 
        "food", 
        "namaste"
    ]
    
    print(f"\n📋 Found {len(data['files'])} total files")
    print(f"🔍 Looking for signs: {needed_signs}\n")
    
    downloaded_count = 0
    total_size = 0
    
    for file_info in data['files']:
        filename = file_info['key']
        file_url = file_info['links']['self']
        file_size = file_info.get('size', 0)
        
        # Check if this file is one we need
        should_download = False
        matched_sign = None
        
        # Convert filename to lowercase for matching
        filename_lower = filename.lower()
        
        for sign in needed_signs:
            sign_lower = sign.lower().replace(" ", "_")
            if sign_lower in filename_lower:
                should_download = True
                matched_sign = sign
                break
        
        if should_download:
            print(f"⬇️ Downloading: {filename}")
            print(f"   Size: {file_size/1024/1024:.2f} MB")
            print(f"   Sign: {matched_sign}")
            
            # Download with progress
            try:
                file_response = requests.get(file_url, stream=True)
                if file_response.status_code == 200:
                    file_path = output_dir / filename
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Download
                    with open(file_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"   ✅ Downloaded successfully")
                    downloaded_count += 1
                    total_size += file_size
                    
                    # Check if it's a zip file and extract
                    if filename.endswith('.zip'):
                        print(f"   📦 Extracting zip file...")
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(output_dir)
                        print(f"   ✅ Extracted")
                        
                else:
                    print(f"   ❌ Failed to download")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Skip other files
        else:
            # Only print for first few files to avoid clutter
            if downloaded_count < 5:
                print(f"⏭️ Skipping: {filename}")
    
    print(f"\n📊 Download Summary:")
    print(f"   Files downloaded: {downloaded_count}")
    print(f"   Total size: {total_size/1024/1024:.2f} MB")
    print(f"   Location: {output_dir.absolute()}")

def get_include_50_signs():
    """
    Get the complete list of INCLUDE-50 signs
    """
    print("\n📋 Fetching INCLUDE-50 sign list...")
    
    try:
        from datasets import load_dataset
        
        # Load the dataset (metadata only)
        dataset = load_dataset("ai4bharat/INCLUDE", split="train", streaming=True)
        
        # Filter for include_50 = True
        include_50 = []
        for item in dataset:
            if item.get('include_50', False):
                include_50.append(item.get('label', ''))
        
        # Get unique signs
        unique_signs = list(set(include_50))
        unique_signs.sort()
        
        print(f"\n✅ Found {len(unique_signs)} INCLUDE-50 signs:")
        for i, sign in enumerate(unique_signs, 1):
            print(f"   {i}. {sign}")
        
        return unique_signs
        
    except Exception as e:
        print(f"❌ Error fetching from HuggingFace: {e}")
        print("   Using fallback list...")
        
        # Fallback list (common signs)
        fallback_list = [
            "thank_you", "yes", "no", "please", "hello", "goodbye",
            "food", "water", "namaste", "toilet", "where", "when",
            "how", "why", "what", "which", "who", "want", "need",
            "help", "sorry", "love", "happy", "sad", "angry",
            "tired", "hungry", "thirsty", "cold", "hot", "pain",
            "doctor", "hospital", "medicine", "money", "time",
            "today", "tomorrow", "yesterday", "week", "month",
            "year", "morning", "evening", "night", "work",
            "school", "home", "family", "friend"
        ]
        return fallback_list

# Check if files already exist
def check_existing_files():
    """Check what files you already have"""
    include_path = Path("INCLUDE-50")
    if include_path.exists():
        files = list(include_path.rglob("*"))
        print(f"\n📂 Existing files in INCLUDE-50:")
        print(f"   Total files: {len(files)}")
        
        # Check for specific signs
        signs_found = set()
        for f in files:
            if f.is_dir():
                for sign in ["thank", "yes", "toilet", "food", "namaste"]:
                    if sign in str(f).lower():
                        signs_found.add(sign)
        
        if signs_found:
            print(f"   Found these signs: {signs_found}")
        else:
            print("   No sign folders found yet")
    else:
        print("\n📂 No existing INCLUDE-50 folder found")

if __name__ == "__main__":
    print("="*60)
    print("INCLUDE-50 Dataset Downloader")
    print("="*60)
    
    # Check what you already have
    check_existing_files()
    
    # Get the full list (optional)
    # include_50_signs = get_include_50_signs()
    
    # Download the dataset
    print("\n🔄 Starting download...")
    download_include_dataset()
    
    print("\n✅ Download process complete!")
    print("\nNext steps:")
    print("1. Check the INCLUDE-50 folder for your files")
    print("2. Run the conversion script to create .npy files")