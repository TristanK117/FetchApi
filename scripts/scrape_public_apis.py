"""
Scraper for Public APIs (GitHub Repository)
Source: Parse README.md from https://github.com/public-apis/public-apis
"""
import requests
import json
import time
import re
from pathlib import Path


def scrape_public_apis():
    """Scrape APIs from the Public APIs GitHub repository README"""
    print("Scraping Public APIs (GitHub README)...")

    url = "https://raw.githubusercontent.com/public-apis/public-apis/master/README.md"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        readme_content = response.text

        # Parse the markdown table
        # Format: | API | Description | Auth | HTTPS | CORS |
        # Find all table rows (skip header and separator)
        lines = readme_content.split('\n')

        apis = []
        current_category = None

        for line in lines:
            # Detect category headers (### Category Name)
            if line.startswith('###'):
                current_category = line.replace('###', '').strip()
                continue

            # Parse table rows
            if line.startswith('| [') and '|' in line:
                # Split by | and clean up
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:  # Valid row
                    # Extract API name from markdown link [Name](URL)
                    api_cell = parts[1]
                    name_match = re.search(r'\[(.*?)\]\((.*?)\)', api_cell)

                    if name_match:
                        name = name_match.group(1)
                        link = name_match.group(2)
                        description = parts[2]
                        auth = parts[3] if len(parts) > 3 else 'No Auth'
                        https = parts[4] if len(parts) > 4 else 'No'
                        cors = parts[5] if len(parts) > 5 else 'Unknown'

                        apis.append({
                            'API': name,
                            'Description': description,
                            'Auth': auth.replace('`', '').strip(),
                            'HTTPS': https.lower() == 'yes',
                            'Cors': cors.replace('`', '').strip(),
                            'Link': link,
                            'Category': current_category or 'General'
                        })

        print(f"Found {len(apis)} APIs from Public APIs")

        # Save raw data
        output_dir = Path(__file__).parent.parent / "data" / "raw"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "public_apis_raw.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'source': 'public_apis',
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                'count': len(apis),
                'apis': apis
            }, f, indent=2, ensure_ascii=False)

        print(f"Saved to {output_file}")
        return apis

    except requests.RequestException as e:
        print(f"Error scraping Public APIs: {e}")
        return []


if __name__ == "__main__":
    scrape_public_apis()
