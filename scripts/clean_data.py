"""
Data cleaning and standardization script
Combines all raw data sources into a standardized format
"""
import json
import csv
import hashlib
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Dict, Any


def load_raw_data():
    """Load all raw data files"""
    raw_dir = Path(__file__).parent.parent / "data" / "raw"
    data_sources = {}

    # Load Public APIs
    public_apis_file = raw_dir / "public_apis_raw.json"
    if public_apis_file.exists():
        with open(public_apis_file, 'r', encoding='utf-8') as f:
            data_sources['public_apis'] = json.load(f)
        print(f"Loaded {data_sources['public_apis']['count']} APIs from Public APIs")

    # Load APIs.guru
    apis_guru_file = raw_dir / "apis_guru_raw.json"
    if apis_guru_file.exists():
        with open(apis_guru_file, 'r', encoding='utf-8') as f:
            data_sources['apis_guru'] = json.load(f)
        print(f"Loaded {data_sources['apis_guru']['count']} APIs from APIs.guru")

    # Load API List
    api_list_file = raw_dir / "api_list_raw.json"
    if api_list_file.exists():
        with open(api_list_file, 'r', encoding='utf-8') as f:
            data_sources['api_list'] = json.load(f)
        print(f"Loaded {data_sources['api_list']['count']} APIs from API List")

    return data_sources


def normalize_public_apis(api_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Public APIs data to standard schema"""
    return {
        'name': api_data.get('API', '').strip(),
        'description': api_data.get('Description', '').strip(),
        'category': api_data.get('Category', '').strip(),
        'auth_type': api_data.get('Auth', 'No Auth').strip(),
        'link': api_data.get('Link', '').strip(),
        'https': api_data.get('HTTPS', False),
        'cors': api_data.get('Cors', 'unknown'),
        'endpoints': [],
        'source': 'public_apis'
    }


def normalize_apis_guru(api_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize APIs.guru data to standard schema"""
    info = api_data.get('info', {})

    # Extract auth type from info if available
    auth_type = 'No Auth'  # Default

    # Get contact/documentation
    link = info.get('contact', {}).get('url', '')
    if not link:
        link = api_data.get('swagger_url', '')

    # Extract category from tags or title
    category = 'General'
    if 'x-apisguru-categories' in info:
        categories = info.get('x-apisguru-categories', [])
        if categories:
            category = categories[0]

    return {
        'name': info.get('title', api_data.get('api_name', '')).strip(),
        'description': info.get('description', '').strip(),
        'category': category,
        'auth_type': auth_type,
        'link': link.strip(),
        'https': True,  # APIs.guru mostly contains HTTPS APIs
        'cors': 'unknown',
        'endpoints': [],
        'version': info.get('version', ''),
        'source': 'apis_guru'
    }


def normalize_api_list(api_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize API List data to standard schema"""
    return {
        'name': api_data.get('API', '').strip(),
        'description': api_data.get('Description', '').strip(),
        'category': api_data.get('Category', '').strip(),
        'auth_type': api_data.get('Auth', 'No Auth').strip(),
        'link': api_data.get('Link', '').strip(),
        'https': api_data.get('HTTPS', False),
        'cors': api_data.get('Cors', 'unknown'),
        'endpoints': [],
        'source': 'api_list'
    }


def is_valid_entry(entry: Dict[str, Any]) -> bool:
    """Validate that an entry has required fields"""
    if not entry.get('name') or not entry.get('description'):
        return False

    # Name and description must be non-empty after stripping
    if len(entry['name']) < 2 or len(entry['description']) < 10:
        return False

    return True


def generate_id(name: str, source: str) -> str:
    """Generate a unique ID for an API"""
    # Create a hash from name and source
    unique_string = f"{name.lower()}_{source}"
    return hashlib.md5(unique_string.encode()).hexdigest()[:12]


def similar(a: str, b: str) -> float:
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_duplicates(apis: List[Dict[str, Any]], threshold: float = 0.85) -> List[int]:
    """Find duplicate APIs by name similarity"""
    to_remove = set()

    for i in range(len(apis)):
        if i in to_remove:
            continue

        for j in range(i + 1, len(apis)):
            if j in to_remove:
                continue

            # Compare names
            similarity = similar(apis[i]['name'], apis[j]['name'])

            if similarity >= threshold:
                # Keep the one with more information (longer description)
                if len(apis[i].get('description', '')) >= len(apis[j].get('description', '')):
                    to_remove.add(j)
                else:
                    to_remove.add(i)
                    break

    return sorted(to_remove, reverse=True)


def clean_and_standardize():
    """Main cleaning and standardization function"""
    print("=" * 60)
    print("Starting data cleaning and standardization...")
    print("=" * 60)
    print()

    # Load raw data
    print("Loading raw data...")
    raw_data = load_raw_data()
    print()

    # Normalize all APIs
    print("Normalizing data to standard schema...")
    normalized_apis = []

    # Process Public APIs
    if 'public_apis' in raw_data:
        for api in raw_data['public_apis']['apis']:
            normalized = normalize_public_apis(api)
            if is_valid_entry(normalized):
                normalized_apis.append(normalized)

    # Process APIs.guru
    if 'apis_guru' in raw_data:
        for api in raw_data['apis_guru']['apis']:
            normalized = normalize_apis_guru(api)
            if is_valid_entry(normalized):
                normalized_apis.append(normalized)

    # Process API List
    if 'api_list' in raw_data:
        for api in raw_data['api_list']['apis']:
            normalized = normalize_api_list(api)
            if is_valid_entry(normalized):
                normalized_apis.append(normalized)

    print(f"Normalized {len(normalized_apis)} APIs")
    print()

    # Remove duplicates
    print("Removing duplicates...")
    duplicates = find_duplicates(normalized_apis)

    for idx in duplicates:
        del normalized_apis[idx]

    print(f"Removed {len(duplicates)} duplicates")
    print(f"Remaining: {len(normalized_apis)} unique APIs")
    print()

    # Add unique IDs
    print("Generating unique IDs...")
    for api in normalized_apis:
        api['id'] = generate_id(api['name'], api['source'])

    # Sort by category then name
    normalized_apis.sort(key=lambda x: (x.get('category', ''), x.get('name', '')))
    print()

    # Save cleaned data as JSON
    print("Saving cleaned data...")
    output_dir = Path(__file__).parent.parent / "data" / "cleaned"
    output_dir.mkdir(parents=True, exist_ok=True)

    json_file = output_dir / "apis_cleaned.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(normalized_apis, f, indent=2, ensure_ascii=False)

    print(f"Saved JSON: {json_file}")

    # Save as CSV for easy inspection
    csv_file = output_dir / "apis_cleaned.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        if normalized_apis:
            fieldnames = ['id', 'name', 'description', 'category', 'auth_type', 'link', 'https', 'cors', 'source']
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(normalized_apis)

    print(f"Saved CSV: {csv_file}")
    print()

    # Generate statistics
    print("=" * 60)
    print("CLEANING COMPLETE")
    print("=" * 60)
    print(f"Total APIs:        {len(normalized_apis)}")

    # Count by source
    sources = {}
    for api in normalized_apis:
        source = api.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1

    print("\nAPIs by source:")
    for source, count in sorted(sources.items()):
        print(f"  {source:20} {count}")

    # Count by category
    categories = {}
    for api in normalized_apis:
        category = api.get('category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1

    print(f"\nCategories:        {len(categories)}")
    print("Top 10 categories:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {category:20} {count}")

    # Count by auth type
    auth_types = {}
    for api in normalized_apis:
        auth = api.get('auth_type', 'Unknown')
        auth_types[auth] = auth_types.get(auth, 0) + 1

    print("\nAuthentication types:")
    for auth, count in sorted(auth_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {auth:20} {count}")


if __name__ == "__main__":
    clean_and_standardize()
