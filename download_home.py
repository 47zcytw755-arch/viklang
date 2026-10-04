import requests
from pathlib import Path
import time
import sys

def download_file(url, filename, output_dir="INCLUDE-50"):
    """
    Download file with progress bar and retry on failure
    """
    output_path = Path(output_dir) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Delete if exists
    if output_path.exists():
        print(f"🗑️ Deleting existing file: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        output_path.unlink()
    
    print(f"📡 Connecting to server...")
    print(f"📦 Downloading: {filename}")
    print("="*50)
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, stream=True, headers=headers, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        print(f"Total file size: {total_size / 1024 / 1024:.1f} MB")
        
        if total_size < 800 * 1024 * 1024:  # Less than 800 MB
            print(f"⚠️ Warning: File seems smaller than expected ({total_size/1024/1024:.1f} MB)")
            print("   Expected: ~833 MB")
            print("   This might be the wrong file or incomplete")
        
        downloaded = 0
        start_time = time.time()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress bar
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        size_mb = downloaded / 1024 / 1024
                        speed = (downloaded / 1024 / 1024) / (time.time() - start_time + 0.001)
                        bar = '█' * int(percent / 2) + '░' * (50 - int(percent / 2))
                        sys.stdout.write(f'\r  {bar} {percent:.1f}% ({size_mb:.1f}/{total_size/1024/1024:.1f} MB) {speed:.1f} MB/s')
                        sys.stdout.flush()
        
        print(f"\n\n✅ Download complete!")
        final_size = output_path.stat().st_size / 1024 / 1024
        print(f"   File: {output_path}")
        print(f"   Size: {final_size:.1f} MB")
        
        if final_size < 800:
            print(f"⚠️ File is still too small ({final_size:.1f} MB)")
            print("   The server might be serving a different file")
            print("   Try downloading from browser instead")
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

if __name__ == "__main__":
    # Zenodo URL for Home_4of4.zip
    record_id = "4010759"
    api_url = f"https://zenodo.org/api/records/{record_id}"
    
    print("📡 Fetching file information...")
    response = requests.get(api_url)
    data = response.json()
    
    # Find Home_4of4.zip
    target_file = None
    for file_info in data['files']:
        if file_info['key'] == 'Home_4of4.zip':
            target_file = file_info
            break
    
    if target_file:
        print(f"✅ Found: {target_file['key']}")
        print(f"   Server size: {target_file['size'] / 1024 / 1024:.1f} MB")
        file_url = target_file['links']['self']
        
        success = download_file(file_url, 'Home_4of4.zip')
        if success:
            print("\n📦 Now extracting...")
            import zipfile
            try:
                with zipfile.ZipFile('INCLUDE-50/Home_4of4.zip', 'r') as zip_ref:
                    zip_ref.extractall('INCLUDE-50/Home')
                print("✅ Extracted to: INCLUDE-50/Home")
                
                # Count videos
                from pathlib import Path
                videos = list(Path('INCLUDE-50/Home').rglob('*.mp4')) + list(Path('INCLUDE-50/Home').rglob('*.avi'))
                print(f"📹 Found {len(videos)} video files")
                
            except Exception as e:
                print(f"❌ Extraction failed: {e}")
    else:
        print("❌ Home_4of4.zip not found in the record")
        print("\nAvailable files:")
        for file_info in data['files']:
            if file_info['key'].endswith('.zip'):
                print(f"  - {file_info['key']} ({file_info['size']/1024/1024:.1f} MB)")