import requests

# Try to get the dataset info from HuggingFace API
api_url = "https://huggingface.co/api/datasets/sign/INCLUDE"
response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Dataset found: {data.get('id')}")
    print(f"   Description: {data.get('description', 'N/A')[:200]}...")
    print(f"   Downloads: {data.get('downloads', 'N/A')}")
else:
    print(f"❌ Dataset not found (status: {response.status_code})")
    print("   The dataset might have a different name or be private")