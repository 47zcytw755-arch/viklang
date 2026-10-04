# get_include50_signs.py
from datasets import load_dataset

print("📡 Fetching INCLUDE-50 sign names from HuggingFace...")
print("="*70)

# Load the dataset
dataset = load_dataset("ai4bharat/INCLUDE", split="train", streaming=True)

# Get all include_50 signs
include_50_labels = []
for item in dataset:
    if item.get('include_50', False):
        label = item.get('label', '')
        if label:
            include_50_labels.append(label)

# Remove duplicates and sort
include_50_labels = sorted(set(include_50_labels))

print(f"\n✅ Found {len(include_50_labels)} INCLUDE-50 signs:")
print("="*70)

# Show all signs with numbers
for i, sign in enumerate(include_50_labels, 1):
    print(f"{i:3d}. {sign}")

# Save to file
with open('include50_signs.txt', 'w') as f:
    for sign in include_50_labels:
        f.write(f"{sign}\n")

print("\n✅ Saved to include50_signs.txt")

# Also create a clean version (without numbers)
clean_signs = []
for sign in include_50_labels:
    # Remove the number prefix (e.g., "55. Thank you" -> "thank_you")
    clean = sign.split('.', 1)[-1].strip().lower().replace(' ', '_')
    clean_signs.append(clean)

print(f"\n📋 Clean sign names (for folder names):")
for sign in clean_signs[:20]:
    print(f"   - {sign}")