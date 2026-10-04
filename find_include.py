import requests

# Search for INCLUDE dataset on Zenodo
search_url = "https://zenodo.org/api/records/?q=INCLUDE sign language&size=10"
response = requests.get(search_url)
results = response.json()

print("Found these datasets:")
for record in results['hits']['hits']:
    print(f"ID: {record['id']}")
    print(f"Title: {record['metadata']['title']}")
    print(f"Files: {record['files'] if 'files' in record else 'N/A'}")
    print("-" * 50)