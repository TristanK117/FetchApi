"""
Scraper for RapidAPI Hub
Source: Popular APIs from RapidAPI's top categories
Manual curated list of well-known free APIs
"""
import json
import time
from pathlib import Path


def scrape_api_list():
    """
    Curated list of popular free APIs
    This supplements our other sources with well-known, reliable APIs
    """
    print("Loading curated API list...")

    # Curated list of popular free APIs (no auth or simple API key)
    apis = [
        {
            "API": "JSONPlaceholder",
            "Description": "Free fake API for testing and prototyping",
            "Category": "Development",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://jsonplaceholder.typicode.com/"
        },
        {
            "API": "OpenWeatherMap",
            "Description": "Weather data including current weather data, forecasts, nowcasts and historical weather data",
            "Category": "Weather",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://openweathermap.org/api"
        },
        {
            "API": "CoinGecko",
            "Description": "Cryptocurrency price, market, and developer data",
            "Category": "Cryptocurrency",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://www.coingecko.com/en/api"
        },
        {
            "API": "REST Countries",
            "Description": "Information about countries via a RESTful API",
            "Category": "Geography",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://restcountries.com"
        },
        {
            "API": "The Cat API",
            "Description": "Pictures of cats from Tumblr",
            "Category": "Animals",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://thecatapi.com/"
        },
        {
            "API": "The Dog API",
            "Description": "Collection of dog pictures",
            "Category": "Animals",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://thedogapi.com/"
        },
        {
            "API": "Unsplash",
            "Description": "Free high-resolution photos",
            "Category": "Photography",
            "Auth": "OAuth",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://unsplash.com/developers"
        },
        {
            "API": "GitHub",
            "Description": "Make use of GitHub repositories, code and user info programmatically",
            "Category": "Development",
            "Auth": "OAuth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://docs.github.com/en/rest"
        },
        {
            "API": "Advice Slip",
            "Description": "Generate random advice slips",
            "Category": "Entertainment",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://api.adviceslip.com/"
        },
        {
            "API": "Bored API",
            "Description": "Find random activities to fight boredom",
            "Category": "Entertainment",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://www.boredapi.com/"
        },
        {
            "API": "Chuck Norris Jokes",
            "Description": "JSON API for hand curated Chuck Norris jokes",
            "Category": "Entertainment",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://api.chucknorris.io/"
        },
        {
            "API": "Google Maps",
            "Description": "Create/customize digital maps based on Google Maps data",
            "Category": "Geocoding",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://developers.google.com/maps/"
        },
        {
            "API": "NewsAPI",
            "Description": "Locate articles and breaking news headlines from news sources and blogs",
            "Category": "News",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://newsapi.org/"
        },
        {
            "API": "PokeAPI",
            "Description": "Pokemon information",
            "Category": "Games",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://pokeapi.co/"
        },
        {
            "API": "Spotify",
            "Description": "View Spotify music catalog, manage users' libraries, get recommendations and more",
            "Category": "Music",
            "Auth": "OAuth",
            "HTTPS": True,
            "Cors": "unknown",
            "Link": "https://developer.spotify.com/documentation/web-api/"
        },
        {
            "API": "Random User Generator",
            "Description": "Generate random user data like name, email, address",
            "Category": "Development",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://randomuser.me/"
        },
        {
            "API": "ExchangeRate-API",
            "Description": "Free currency conversion",
            "Category": "Finance",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://www.exchangerate-api.com/"
        },
        {
            "API": "JokeAPI",
            "Description": "Programming, miscellaneous, dark and spooky jokes",
            "Category": "Entertainment",
            "Auth": "No Auth",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://jokeapi.dev/"
        },
        {
            "API": "Numbers API",
            "Description": "Facts about numbers",
            "Category": "Science",
            "Auth": "No Auth",
            "HTTPS": False,
            "Cors": "yes",
            "Link": "http://numbersapi.com/"
        },
        {
            "API": "NASA",
            "Description": "NASA data, including imagery",
            "Category": "Science",
            "Auth": "API Key",
            "HTTPS": True,
            "Cors": "yes",
            "Link": "https://api.nasa.gov/"
        }
    ]

    print(f"Loaded {len(apis)} curated APIs")

    # Save raw data
    output_dir = Path(__file__).parent.parent / "data" / "raw"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "api_list_raw.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'api_list_curated',
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'count': len(apis),
            'apis': apis
        }, f, indent=2, ensure_ascii=False)

    print(f"Saved to {output_file}")
    return apis


if __name__ == "__main__":
    scrape_api_list()
