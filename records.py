import json
import requests

from pathlib import Path

source_url = "https://api.tvmaze.com/shows?page=0"
output = Path("summary.json")

def fetch_records(url):
    """Download TV show records and return them as Python objects"""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()

def shows_per_genre(records):
    """Count how many shows belong to each genre."""
    genre_shows_count = {}

    for show in records:
        genres = show.get("genres") or []

        for genre in genres:
            genre_shows_count[genre] = genre_shows_count.get(genre, 0) + 1

    return genre_shows_count

def average_rating_by_language(records):
    """Calculate the average show rating for each language"""
    ratings_by_language = {}

    for show in records:
        language = show.get("language")
        rating_data = show.get("rating") or {}
        rating = rating_data.get("average")

        if not language or rating is None:
            continue

        if language not in ratings_by_language:
            ratings_by_language[language] = []

        ratings_by_language[language].append(rating)

    return {
        language: round(sum(ratings) / len(ratings), 2)
        for language, ratings in ratings_by_language.items()
    }

def shows_per_network(records):
    """Count how many shows belong to each network."""
    network_counts = {}

    for show in records:
        network = show.get("network")

        if network and network.get("name"):
            network_name = network["name"]
        else:
            network_name = "No Network"

        network_counts[network_name] = network_counts.get(network_name, 0) + 1

    return network_counts

def shows_per_decade(records):
    """Count how many shows premiered in each decade."""
    decade_counts = {}

    for show in records:
        premiered = show.get("premiered")

        if not premiered or len(premiered) < 4:
            continue

        year_text = premiered[:4]

        if not year_text.isdigit():
            continue

        year = int(year_text)
        decade = (year // 10) * 10
        decade_name = f"{decade}s"

        decade_counts[decade_name] = decade_counts.get(decade_name, 0) + 1

    return decade_counts

def data_quirks(records):
    """Summarize missing values and unique languages found in the dataset."""
    shows_without_genres = 0
    shows_without_rating = 0
    shows_without_network = 0
    shows_without_premiered_date = 0

    unique_languages = set()

    for show in records:
        if not show.get("genres"):
            shows_without_genres += 1

        rating_data = show.get("rating") or {}
        if rating_data.get("average") is None:
            shows_without_rating += 1

        if not show.get("network"):
            shows_without_network += 1

        if not show.get("premiered"):
            shows_without_premiered_date += 1

        language = show.get("language")
        if language:
            unique_languages.add(language)

    return {
        "shows_without_genres": shows_without_genres,
        "shows_without_rating": shows_without_rating,
        "shows_without_network": shows_without_network,
        "shows_without_premiered_date": shows_without_premiered_date,
        "unique_languages": sorted(unique_languages),
    }

def build_summary(records):
    """Combine all aggregations into one dictionary ready to write."""
    return {
        "source_url": source_url,
        "records_processed": len(records),
        "shows_per_genre": shows_per_genre(records),
        "average_rating_by_language": average_rating_by_language(records),
        "shows_per_network": shows_per_network(records),
        "shows_per_decade": shows_per_decade(records),
        "data_quirks": data_quirks(records),
    }


def write_summary(summary, path):
    """Write the summary to a JSON file"""
    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2)
    except OSError as error:
        print(f"Could not write summary to {path}: {error}")
        return False
    return True    


def main():
    try:
        records = fetch_records(source_url)

    except (requests.RequestException, ValueError) as error:
        print(f"Could not download TV show data: {error}")
        return

    summary = build_summary(records)

    print(f"\nDownloaded {len(records)} records from {source_url}")
    print(f"\nSummary of TV show data: {summary}")
    if write_summary(summary, output):
        print(f"\nSummary written to {output}\n")


if __name__ == "__main__":
    main()
