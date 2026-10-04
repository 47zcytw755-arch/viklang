# convert_category_signs.py
import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import time
import sys

class CategoryConverter:
    def __init__(self):
        print("🔄 Initializing MediaPipe...")
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        print("✅ MediaPipe initialized")
    
    def extract_features(self, results):
        features = []
        
        if results.left_hand_landmarks:
            for lm in results.left_hand_landmarks.landmark:
                features.extend([lm.x, lm.y, lm.z])
        else:
            features.extend([0.0] * 63)
        
        if results.right_hand_landmarks:
            for lm in results.right_hand_landmarks.landmark:
                features.extend([lm.x, lm.y, lm.z])
        else:
            features.extend([0.0] * 63)
        
        return features
    
    def process_video(self, video_path, output_dir, sequence_id):
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames < 10:
            cap.release()
            return None
        
        frame_indices = np.linspace(0, total_frames - 1, 30, dtype=int)
        sequence = []
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            
            if not ret:
                sequence.append([0.0] * 126)
                continue
            
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.holistic.process(rgb)
            features = self.extract_features(results)
            sequence.append(features)
        
        cap.release()
        
        while len(sequence) < 30:
            sequence.append([0.0] * 126)
        sequence = np.array(sequence[:30])
        
        output_path = output_dir / f"{sequence_id}.npy"
        np.save(output_path, sequence)
        return output_path
    
    def convert_category(self, category_path, max_videos_per_sign=10):
        """Convert all signs in a category folder"""
        category_path = Path(category_path)
        category_name = category_path.name
        
        print(f"\n📂 Processing Category: {category_name}")
        print("-"*60)
        
        # Find all subfolders (these are the actual signs)
        sign_folders = [f for f in category_path.iterdir() if f.is_dir()]
        
        if not sign_folders:
            print(f"   ⚠️ No subfolders found in {category_name}")
            return 0
        
        print(f"   Found {len(sign_folders)} signs in this category")
        
        total_converted = 0
        
        for sign_folder in sign_folders:
            sign_name = sign_folder.name.replace('_', ' ').lower()
            
            # Output directory
            output_dir = Path("lstm_data") / sign_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Find videos
            videos = list(sign_folder.rglob('*.mp4')) + list(sign_folder.rglob('*.avi'))
            
            if not videos:
                print(f"   ⚠️ No videos in: {sign_name}")
                continue
            
            # Get existing sequences
            existing = list(output_dir.glob("*.npy"))
            sequence_id = len(existing)
            
            # Convert up to max_videos_per_sign
            convert_count = min(len(videos), max_videos_per_sign)
            converted = 0
            
            print(f"\n   📹 Converting: {sign_name}")
            print(f"      Found {len(videos)} videos, converting {convert_count}")
            
            for i, video_path in enumerate(videos[:convert_count], 1):
                print(f"      [{i}/{convert_count}] {video_path.name}")
                result = self.process_video(video_path, output_dir, sequence_id)
                if result:
                    sequence_id += 1
                    converted += 1
            
            if converted > 0:
                print(f"      ✅ Converted {converted} sequences for '{sign_name}'")
                total_converted += converted
            else:
                print(f"      ❌ Failed to convert any videos for '{sign_name}'")
        
        return total_converted

def main():
    print("="*70)
    print("🔄 Convert Category Signs to .npy")
    print("="*70)
    
    include_path = Path("INCLUDE-50-ALL")
    
    if not include_path.exists():
        print(f"❌ Path not found: {include_path}")
        return
    
    # Categories to convert
    categories = [
        "Animals",
        "Colours", 
        "Days_and_Time",
        "Home",
        "Jobs",
        "People",
        "Society"
    ]
    
    print(f"📂 Converting {len(categories)} categories")
    print(f"   Categories: {', '.join(categories)}")
    
    converter = CategoryConverter()
    total_converted = 0
    
    for category in categories:
        category_path = include_path / category
        
        if not category_path.exists():
            print(f"\n❌ Category not found: {category}")
            continue
        
        converted = converter.convert_category(category_path)
        total_converted += converted
    
    print("\n" + "="*70)
    print("📊 Conversion Complete!")
    print("="*70)
    print(f"✅ Total new sequences converted: {total_converted}")
    
    # Show what you have now
    print("\n📁 Updated Dataset Summary:")
    lstm_path = Path("lstm_data")
    if lstm_path.exists():
        total_signs = 0
        total_sequences = 0
        for folder in sorted(lstm_path.iterdir()):
            if folder.is_dir():
                npy_files = list(folder.glob("*.npy"))
                if npy_files:
                    total_signs += 1
                    total_sequences += len(npy_files)
                    print(f"   ✅ {folder.name}: {len(npy_files)} sequences")
        
        print("="*70)
        print(f"📊 Total signs: {total_signs}")
        print(f"📹 Total sequences: {total_sequences}")
        print("="*70)

if __name__ == "__main__":
    main()