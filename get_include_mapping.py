# create_complete_mapping.py
from pathlib import Path

print("🔄 Creating complete mapping for INCLUDE-50 signs")
print("="*70)

# The complete INCLUDE-50 sign mapping (folder_name -> clean_sign_name)
sign_mapping = {
    "1. dog": "dog",
    "1. loud": "loud",
    "11. car": "car",
    "14. election": "election",
    "16. train ticket": "train_ticket",
    "19. house": "house",
    "2. death": "death",
    "2. quiet": "quiet",
    "23. court": "court",
    "28. store or shop": "store_or_shop",
    "28. window": "window",
    "3. happy": "happy",
    "34. pen": "pen",
    "35. bank": "bank",
    "37. hat": "hat",
    "4. bird": "bird",
    "40. i": "i",
    "40. paint": "paint",
    "42. t-shirt": "t_shirt",
    "44. shoes": "shoes",
    "44. it": "it",
    "46. you (plural)": "you_plural",
    "47. red": "red",
    "48. hello": "hello",
    "5. cow": "cow",
    "51. good morning": "good_morning",
    "53. fan": "fan",
    "54. black": "black",
    "54. cell phone": "cell_phone",
    "55. thank you": "thank_you",
    "55. white": "white",
    "61. father": "father",
    "61. summer": "summer",
    "64. fall": "fall",
    "66. brother": "brother",
    "67. monday": "monday",
    "77. boy": "boy",
    "78. girl": "girl",
    "78. year": "year",
    "78. long": "long",
    "79. short": "short",
    "83. big large": "big_large",
    "84. teacher": "teacher",
    "84. small little": "small_little",
    "86. time": "time",
    "87. hot": "hot",
    "91. priest": "priest",
    "91. new": "new",
    "94. good": "good",
    "97. dry": "dry"
}

print(f"✅ Created mapping for {len(sign_mapping)} signs")

# Show first 10 mappings
print("\n📋 First 10 mappings:")
for i, (old, new) in enumerate(list(sign_mapping.items())[:10], 1):
    print(f"   {i:2d}. {old} -> {new}")

# Save mapping
import json
with open('include50_mapping_complete.json', 'w') as f:
    json.dump(sign_mapping, f, indent=2)

print("\n✅ Mapping saved to include50_mapping_complete.json")