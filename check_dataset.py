# check_dataset.py
import numpy as np
from pathlib import Path

lstm_path = Path("lstm_data")

print("📊 Dataset Verification")
print("="*60)

total_sequences = 0
total_signs = 0

for sign_folder in sorted(lstm_path.iterdir()):
    if sign_folder.is_dir():
        npy_files = list(sign_folder.glob("*.npy"))
        
        if npy_files:
            total_signs += 1
            total_sequences += len(npy_files)
            
            # Check first file
            sample = np.load(npy_files[0])
            print(f"\n✅ {sign_folder.name}:")
            print(f"   📹 {len(npy_files)} sequences")
            print(f"   📐 Shape: {sample.shape}")
            print(f"   📊 Data type: {sample.dtype}")
            print(f"   📁 Location: {sign_folder}")
        else:
            print(f"\n❌ {sign_folder.name}: No .npy files!")

print("\n" + "="*60)
print(f"📊 Total signs: {total_signs}")
print(f"📹 Total sequences: {total_sequences}")
print("="*60)