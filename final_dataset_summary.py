# final_dataset_summary.py
from pathlib import Path
import numpy as np

lstm_path = Path("lstm_data")

print("🎯 COMPLETE DATASET SUMMARY")
print("="*70)

total_sequences = 0
signs_data = {}

for folder in sorted(lstm_path.iterdir()):
    if folder.is_dir():
        npy_files = list(folder.glob("*.npy"))
        count = len(npy_files)
        if count > 0:
            signs_data[folder.name] = count
            total_sequences += count

print(f"📊 Total signs: {len(signs_data)}")
print(f"📹 Total sequences: {total_sequences}")
print("="*70)

# Show first 20 signs
print("\n📋 First 20 signs:")
for i, (sign, count) in enumerate(list(signs_data.items())[:20], 1):
    print(f"   {i:2d}. {sign}: {count} sequences")

# Check if all INCLUDE-50 signs are present
include_50_expected = [
    "thank you", "yes", "no", "please", "hello", "goodbye",
    "food", "water", "namaste", "toilet", "where", "when",
    "how", "why", "what", "which", "who", "want", "need",
    "help", "sorry", "love", "happy", "sad", "angry",
    "tired", "hungry", "thirsty", "cold", "hot", "pain",
    "doctor", "hospital", "medicine", "money", "time",
    "today", "tomorrow", "yesterday", "week", "month",
    "year", "morning", "evening", "night", "work",
    "school", "home", "family", "friend"
]

# Check which INCLUDE-50 signs are missing
missing = []
for sign in include_50_expected:
    if sign not in signs_data:
        missing.append(sign)

if missing:
    print(f"\n⚠️ Missing {len(missing)} INCLUDE-50 signs:")
    for sign in missing[:10]:  # Show first 10 missing
        print(f"   - {sign}")
else:
    print("\n🎉 All 50 INCLUDE-50 signs are present!")