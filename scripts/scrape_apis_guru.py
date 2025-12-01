"""
Scraper for APIs.guru
Source: https://api.apis.guru/v2/list.json
"""
import requests
import json
import time
from pathlib import Path


def scrape_apis_guru():
    """Scrape APIs from APIs.guru OpenAPI directory"""
    print("Scraping APIs.guru...")

    url = "https://api.apis.guru/v2/list.json"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        data = response.json()

        # APIs.guru returns a dictionary with API names as keys
        apis = []
        for api_name, api_info in data.items():
            # Get the preferred version or first available version
            versions = api_info.get('versions', {})
            if versions:
                # Get the preferred version
                preferred = api_info.get('preferred')
                if preferred and preferred in versions:
                    version_data = versions[preferred]
                else:
                    # Get first version
                    version_data = list(versions.values())[0]

                apis.append({
                    'api_name': api_name,
                    'info': version_data.get('info', {}),
                    'swagger_url': version_data.get('swaggerUrl'),
                    'swagger_yaml_url': version_data.get('swaggerYamlUrl'),
                    'updated': version_data.get('updated'),
                    'preferred_version': preferred,
                    'all_versions': list(versions.keys())
                })

        print(f"Found {len(apis)} APIs from APIs.guru")

        # Save raw data
        output_dir = Path(__file__).parent.parent / "data" / "raw"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "apis_guru_raw.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'source': 'apis_guru',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'count': len(apis),
                'apis': apis
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved to {output_file}")
        return apis

    except requests.RequestException as e:
        print(f"Error scraping APIs.guru: {e}")
        return []


if __name__ == "__main__":
    scrape_apis_guru()
