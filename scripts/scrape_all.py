"""
Master scraper - runs all individual scrapers
"""
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from scrape_public_apis import scrape_public_apis
from scrape_apis_guru import scrape_apis_guru
from scrape_api_list import scrape_api_list


def main():
    """Run all scrapers"""
    print("=" * 60)
    print("Starting data collection from all sources...")
    print("=" * 60)
    print()

    # Track results
    results = {}

    # Scrape from all sources
    print("[1/3] Public APIs (GitHub)")
    print("-" * 60)
    results['public_apis'] = scrape_public_apis()
    print()

    print("[2/3] APIs.guru")
    print("-" * 60)
    results['apis_guru'] = scrape_apis_guru()
    print()

    print("[3/3] Curated Popular APIs")
    print("-" * 60)
    results['api_list'] = scrape_api_list()
    print()

    # Summary
    print("=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Public APIs (GitHub):  {len(results.get('public_apis', []))} APIs")
    print(f"APIs.guru:             {len(results.get('apis_guru', []))} APIs")
    print(f"Curated APIs:          {len(results.get('api_list', []))} APIs")
    print(f"Total collected: {sum(len(v) for v in results.values())} APIs")
    print()
    print("Raw data saved to data/raw/")
    print("Next step: Run 'python scripts/clean_data.py' to standardize the data")


if __name__ == "__main__":
    main()
