import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import time
import sys
import re

class IncludeToNpyConverter:
    def __init__(self):
        print("🔄 Initializing MediaPipe...")
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✅ MediaPipe initialized")
    
    def extract_features(self, results):
        """Extract features matching your collect_sequences.py format"""
        features = []
        
        # Left hand (21 landmarks × 3 coords = 63 values)
        if results.left_hand_landmarks:
            for lm in results.left_hand_landmarks.landmark:
                features.extend([lm.x, lm.y, lm.z])
        else:
            features.extend([0.0] * 63)
        
        # Right hand (21 landmarks × 3 coords = 63 values)
        if results.right_hand_landmarks:
            for lm in results.right_hand_landmarks.landmark:
                features.extend([lm.x, lm.y, lm.z])
        else:
            features.extend([0.0] * 63)
        
        return features
    
    def find_videos_for_sign(self, include_path, keywords):
        """Find videos for a specific sign with safe pattern matching"""
        include_path = Path(include_path)
        videos = []
        
        # Build a regex pattern from keywords
        pattern_parts = []
        for keyword in keywords:
            # Escape special characters
            escaped = re.escape(keyword)
            pattern_parts.append(escaped)
        
        # Create a combined pattern
        pattern = re.compile('|'.join(pattern_parts), re.IGNORECASE)
        
        # Walk through all files
        for file_path in include_path.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext in ['.mp4', '.avi', '.mov', '.mkv']:
                    # Check if filename or parent folder matches pattern
                    file_str = str(file_path).lower()
                    parent_str = str(file_path.parent).lower()
                    
                    if pattern.search(file_str) or pattern.search(parent_str):
                        videos.append(file_path)
        
        return videos
    
    def process_video(self, video_path, output_dir, sequence_id):
        """Process a single video and save as .npy"""
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames < 10:
            cap.release()
            return None
        
        # Sample 30 frames uniformly
        frame_indices = np.linspace(0, total_frames - 1, 30, dtype=int)
        sequence = []
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if not ret:
                sequence.append([0.0] * 126)
                continue
            
            # Process frame
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.holistic.process(rgb)
            
            features = self.extract_features(results)
            sequence.append(features)
        
        cap.release()
        
        # Ensure exactly 30 frames
        while len(sequence) < 30:
            sequence.append([0.0] * 126)
        sequence = np.array(sequence[:30])
        
        # Save
        output_path = output_dir / f"{sequence_id}.npy"
        np.save(output_path, sequence)
        return output_path
    
    def convert_sign(self, include_path, sign_name, keywords, output_dir):
        """Convert all videos for a specific sign"""
        print(f"\n📹 Searching for '{sign_name}'...")
        print(f"   Keywords: {keywords}")
        
        # Find videos
        videos = self.find_videos_for_sign(include_path, keywords)
        
        if not videos:
            print(f"   ❌ No videos found for '{sign_name}'")
            # Show what's available in the folder structure
            include_path = Path(include_path)
            print(f"\n   📂 Available folders in {include_path}:")
            for folder in include_path.iterdir():
                if folder.is_dir():
                    videos_count = len(list(folder.rglob('*.mp4'))) + len(list(folder.rglob('*.avi')))
                    if videos_count > 0:
                        print(f"      📁 {folder.name}: {videos_count} videos")
            return 0
        
        print(f"   ✅ Found {len(videos)} videos")
        
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get existing sequences
        existing = list(output_dir.glob("*.npy"))
        sequence_id = len(existing)
        
        converted = 0
        for i, video_path in enumerate(videos, 1):
            print(f"   [{i}/{len(videos)}] Processing: {video_path.name}")
            
            result = self.process_video(video_path, output_dir, sequence_id)
            if result:
                sequence_id += 1
                converted += 1
                print(f"      ✅ Saved: {result.name}")
            else:
                print(f"      ⚠️ Failed")
        
        return converted

def explore_folder_structure():
    """Helper function to explore what's in the INCLUDE folder"""
    include_path = Path("INCLUDE-50-ALL")
    
    if not include_path.exists():
        print("❌ INCLUDE-50-ALL folder not found!")
        return
    
    print("\n📂 Exploring INCLUDE-50-ALL structure:")
    print("="*60)
    
    for folder in include_path.iterdir():
        if folder.is_dir():
            print(f"\n📁 {folder.name}:")
            
            # Check subfolders
            subfolders = [f for f in folder.iterdir() if f.is_dir()]
            if subfolders:
                for sub in subfolders:
                    videos = list(sub.rglob('*.mp4')) + list(sub.rglob('*.avi'))
                    if videos:
                        print(f"   └── {sub.name}: {len(videos)} videos")
            else:
                videos = list(folder.rglob('*.mp4')) + list(folder.rglob('*.avi'))
                if videos:
                    print(f"   └── {len(videos)} videos in root")

def main():
    print("="*70)
    print("🔄 INCLUDE-50 to .npy Converter (Fixed)")
    print("="*70)
    
    # First, explore the structure
    print("\n🔍 Let's first explore your folder structure...")
    explore_folder_structure()
    
    # Path
    include_path = input("\n📂 Enter path to INCLUDE-50-ALL folder (or press Enter for default): ").strip()
    if not include_path:
        include_path = "INCLUDE-50-ALL"
    
    if not Path(include_path).exists():
        print(f"❌ Path not found: {include_path}")
        return
    
    print(f"✅ Using: {include_path}")
    
    # Sign mapping with multiple keywords for better matching
    sign_mapping = {
        "thankyou": {
            "keywords": ["thank", "thanks", "thank_you", "thank you"],
            "folder": "thankyou"
        },
        "yes": {
            "keywords": ["yes"],
            "folder": "yes"
        },
        "namaste": {
            "keywords": ["namaste", "namaskar"],
            "folder": "namaste"
        },
        "toilet": {
            "keywords": ["toilet", "bathroom", "washroom", "wc"],
            "folder": "toilet"
        },
        "food": {
            "keywords": ["food", "eat", "meal", "dinner", "lunch"],
            "folder": "food"
        }
    }
    
    print("\n" + "="*70)
    print("📋 Signs to convert:")
    for sign_name in sign_mapping.keys():
        print(f"   - {sign_name}")
    print("="*70)
    
    # Confirm
    response = input("\n🔄 Start conversion? (y/n): ")
    if response.lower() != 'y':
        print("❌ Cancelled")
        return
    
    converter = IncludeToNpyConverter()
    total_converted = 0
    
    for sign_name, sign_info in sign_mapping.items():
        output_dir = Path("lstm_data") / sign_info["folder"]
        output_dir.mkdir(parents=True, exist_ok=True)
        
        converted = converter.convert_sign(
            include_path,
            sign_name,
            sign_info["keywords"],
            output_dir
        )
        total_converted += converted
    
    # Summary
    print("\n" + "="*70)
    print("📊 Conversion Complete!")
    print("="*70)
    print(f"✅ Total .npy files created: {total_converted}")
    print("\n📁 Dataset locations:")
    for sign_name, sign_info in sign_mapping.items():
        folder = Path("lstm_data") / sign_info["folder"]
        npy_files = list(folder.glob("*.npy"))
        print(f"   📁 {folder}: {len(npy_files)} sequences")
    
    print("\n💡 Next steps:")
    print("   1. Run check_dataset.py to verify all files")
    print("   2. Use collect_sequences.py to add more data if needed")

if __name__ == "__main__":
    main()