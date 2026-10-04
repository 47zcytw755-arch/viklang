# convert_all_50_complete.py
import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
import re

class CompleteIncludeConverter:
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
    
    def convert_all_folders(self, include_path):
        """Convert all folders in INCLUDE-50-ALL"""
        include_path = Path(include_path)
        
        print("\n🔍 Finding all sign folders...")
        print("="*70)
        
        # Get all folders with videos
        sign_folders = []
        for folder in include_path.iterdir():
            if folder.is_dir():
                videos = list(folder.rglob('*.mp4')) + list(folder.rglob('*.avi'))
                if videos:
                    sign_folders.append((folder, videos))
        
        print(f"✅ Found {len(sign_folders)} folders with videos")
        
        if len(sign_folders) == 0:
            # Try deeper search
            print("\n🔍 Searching deeper...")
            for folder in include_path.rglob('*'):
                if folder.is_dir():
                    videos = list(folder.rglob('*.mp4')) + list(folder.rglob('*.avi'))
                    if videos and folder.name not in ['videos', 'data']:
                        sign_folders.append((folder, videos))
            
            print(f"✅ Found {len(sign_folders)} folders with videos")
        
        total_converted = 0
        
        for i, (folder, videos) in enumerate(sign_folders, 1):
            # Create sign name from folder
            sign_name = folder.name.replace('_', ' ').lower()
            output_dir = Path("lstm_data") / sign_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            print(f"\n[{i}/{len(sign_folders)}] 📹 {sign_name}")
            print(f"   📁 {folder.name}")
            print(f"   📹 {len(videos)} videos")
            
            # Get existing sequences
            existing = list(output_dir.glob("*.npy"))
            sequence_id = len(existing)
            
            converted = 0
            for video_path in videos[:10]:  # Limit to 10 videos per sign to save time
                result = self.process_video(video_path, output_dir, sequence_id)
                if result:
                    sequence_id += 1
                    converted += 1
            
            total_converted += converted
            print(f"   ✅ Converted: {converted} sequences")

def main():
    print("="*70)
    print("🔄 Convert ALL INCLUDE-50 Signs")
    print("="*70)
    
    # Path to INCLUDE-50-ALL
    include_path = input("\n📂 Enter path to INCLUDE-50-ALL folder: ").strip()
    if not include_path:
        include_path = "INCLUDE-50-ALL"
    
    if not Path(include_path).exists():
        print(f"❌ Path not found: {include_path}")
        return
    
    print(f"✅ Using: {include_path}")
    
    converter = CompleteIncludeConverter()
    converter.convert_all_folders(include_path)
    
    print("\n" + "="*70)
    print("📊 Conversion Complete!")
    print("="*70)
    
    # Show what was created
    lstm_path = Path("lstm_data")
    if lstm_path.exists():
        total_signs = 0
        total_sequences = 0
        for folder in lstm_path.iterdir():
            if folder.is_dir():
                npy_files = list(folder.glob("*.npy"))
                if npy_files:
                    total_signs += 1
                    total_sequences += len(npy_files)
        
        print(f"✅ Total signs: {total_signs}")
        print(f"📹 Total sequences: {total_sequences}")

if __name__ == "__main__":
    main()