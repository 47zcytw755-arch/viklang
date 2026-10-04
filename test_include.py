try:
    from datasets import load_dataset
    
    print("📡 Loading dataset from HuggingFace...")
    dataset = load_dataset("ai4bharat/INCLUDE", split="train")
    
    # Get all signs with include_50 = True
    include_50_signs = []
    count = 0
    
    for item in dataset:
        if item.get('include_50', False):
            include_50_signs.append(item.get('label', ''))
        count += 1
        if count % 1000 == 0:
            print(f"   Processed {count} items...")
    
    # Get unique signs
    unique_signs = set(include_50_signs)
    
    print(f"\n✅ Found {len(unique_signs)} INCLUDE-50 signs:")
    print("-" * 40)
    
    # Sort and display
    for i, sign in enumerate(sorted(unique_signs), 1):
        print(f"{i:3d}. {sign}")
    
    # Check if your signs are in the list
    your_signs = ["thank", "yes", "toilet", "food", "namaste"]
    print("\n" + "="*40)
    print("🔍 Checking your specific signs:")
    
    for sign in your_signs:
        found = [s for s in unique_signs if sign.lower() in s.lower()]
        if found:
            print(f"✅ '{sign}' found as: {found[0]}")
        else:
            print(f"❌ '{sign}' not found in INCLUDE-50")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nTrying alternative method...")
    
    # Alternative: Use the HuggingFace API directly
    import requests
    
    try:
        api_url = "https://huggingface.co/api/datasets/ai4bharat/INCLUDE"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dataset found: {data.get('id')}")
            print(f"   Downloads: {data.get('downloads', 'N/A')}")
            print(f"   Size: {data.get('cardData', {}).get('size', 'N/A')}")
        else:
            print(f"❌ Dataset not accessible (status: {response.status_code})")
    except Exception as e2:
        print(f"❌ Alternative method failed: {e2}")