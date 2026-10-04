import requests
import zipfile
import os
from pathlib import Path
import time
import sys

def download_include50_only():
    """
    Download ONLY the files that contain INCLUDE-50 signs
    """
    output_dir = Path("INCLUDE-50-ALL")
    output_dir.mkdir(exist_ok=True)
    
    # These are the exact files containing INCLUDE-50 signs
    # Based on the dataset structure
    include50_files = [
        ("Greetings_1of2.zip", 0.6),
        ("Greetings_2of2.zip", 0.5),
        ("Home_1of4.zip", 0.8),
        ("Home_2of4.zip", 0.7),
        ("Home_3of4.zip", 0.6),
        ("Home_4of4.zip", 0.5),
        ("Society_1of3.zip", 0.4),
        ("Society_2of3.zip", 0.3),
        ("People_1of5.zip", 0.4),
        ("People_2of5.zip", 0.3),
        ("Adjectives_1of8.zip", 0.4),
        ("Adjectives_2of8.zip", 0.3),
        ("Days_and_Time_1of3.zip", 0.3),
        ("Colours_1of2.zip", 0.2),
        ("Animals_1of2.zip", 0.3),
        ("Jobs_1of2.zip", 0.3),
        ("Pronouns_1of2.zip", 0.2)
    ]
    
    record_id = "4010759"
    total_size = sum(size for _, size in include50_files)
    
    print("="*60)
    print("📥 INCLUDE-50 Selective Downloader")
    print("="*60)
    print(f"📦 Files to download: {len(include50_files)}")
    print(f"📊 Total size: {total_size:.1f} GB")
    print("="*60)
    
    # Confirm
    response = input(f"\n⚠️ This will download ~{total_size:.1f} GB. Continue? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return
    
    downloaded = []
    failed = []
    
    for filename, expected_size_gb in include50_files:
        file_path = output_dir / filename
        expected_size_mb = expected_size_gb * 1024
        
        print(f"\n📦 {filename} ({expected_size_gb:.1f} GB)")
        
        # Check if already downloaded
        if file_path.exists():
            actual_size_mb = file_path.stat().st_size / 1024 / 1024
            if actual_size_mb >= expected_size_mb * 0.8:  # 80% or more
                print(f"   ✅ Already downloaded ({actual_size_mb:.1f} MB)")
                downloaded.append(filename)
                
                # Extract if not extracted
                extract_dir = output_dir / filename.replace('.zip', '')
                if not extract_dir.exists() or not list(extract_dir.glob('*')):
                    print(f"   📦 Extracting...")
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(output_dir)
                        print(f"   ✅ Extracted")
                    except Exception as e:
                        print(f"   ❌ Extraction failed: {e}")
                else:
                    print(f"   ✅ Already extracted")
                continue
            else:
                print(f"   🔄 Incomplete ({actual_size_mb:.1f} MB), re-downloading...")
                file_path.unlink()
        
        # Download
        print(f"   ⬇️ Downloading...")
        url = f"https://zenodo.org/records/{record_id}/files/{filename}?download=1"
        
        try:
            response = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            total_size_bytes = int(response.headers.get('content-length', 0))
            downloaded_bytes = 0
            start_time = time.time()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_bytes += len(chunk)
                        
                        if downloaded_bytes % (1024 * 1024) == 0:
                            elapsed = time.time() - start_time
                            if elapsed > 0:
                                percent = (downloaded_bytes / total_size_bytes) * 100 if total_size_bytes > 0 else 0
                                speed = (downloaded_bytes / 1024 / 1024) / elapsed
                                sys.stdout.write(f'\r   Progress: {percent:.1f}% ({downloaded_bytes/1024/1024:.1f} MB) {speed:.1f} MB/s')
                                sys.stdout.flush()
            
            print(f"\n   ✅ Downloaded ({file_path.stat().st_size/1024/1024:.1f} MB)")
            downloaded.append(filename)
            
            # Extract
            print(f"   📦 Extracting...")
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(output_dir)
                print(f"   ✅ Extracted")
            except Exception as e:
                print(f"   ❌ Extraction failed: {e}")
                failed.append(filename)
                
        except Exception as e:
            print(f"\n   ❌ Failed: {e}")
            failed.append(filename)
    
    # Summary
    print("\n" + "="*60)
    print("📊 Download Summary")
    print("="*60)
    print(f"✅ Downloaded: {len(downloaded)} files")
    print(f"❌ Failed: {len(failed)} files")
    
    if failed:
        print("\n❌ Failed files (download manually):")
        for f in failed:
            print(f"   - {f}")
            print(f"     URL: https://zenodo.org/records/{record_id}/files/{f}?download=1")
    
    # Count videos
    print("\n📁 Extracted content:")
    total_videos = 0
    for folder in output_dir.iterdir():
        if folder.is_dir():
            videos = list(folder.rglob('*.mp4')) + list(folder.rglob('*.avi'))
            if videos:
                total_videos += len(videos)
                print(f"   - {folder.name}: {len(videos)} videos")
    
    print(f"\n📹 Total videos: {total_videos}")

if __name__ == "__main__":
    download_include50_only()