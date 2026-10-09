class Aggregation:
    """Define the common interface for summary calculations."""

    def __init__(self, key):
        self.key = key

    def compute(self, records):
        raise NotImplementedError("Subclasses must implement compute().")


class ShowsPerGenre(Aggregation):
    """Count how many shows belong to each genre."""

    def __init__(self):
        super().__init__("shows_per_genre")

    def compute(self, records):
        genre_counts = {}

        for show in records:
            for genre in show.genres:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        return genre_counts


class AverageRatingByLanguage(Aggregation):
    """Calculate the average show rating for each language."""

    def __init__(self):
        super().__init__("average_rating_by_language")

    def compute(self, records):
        ratings_by_language = {}

        for show in records:
            if not show.language or show.rating is None:
                continue

            if show.language not in ratings_by_language:
                ratings_by_language[show.language] = []

            ratings_by_language[show.language].append(show.rating)

        return {
            language: round(sum(ratings) / len(ratings), 2)
            for language, ratings in ratings_by_language.items()
        }


class ShowsPerNetwork(Aggregation):
    """Count how many shows belong to each network."""

    def __init__(self):
        super().__init__("shows_per_network")

    def compute(self, records):
        network_counts = {}

        for show in records:
            network_name = show.network_name
            network_counts[network_name] = (
                network_counts.get(network_name, 0) + 1
            )

        return network_counts


class ShowsPerDecade(Aggregation):
    """Count how many shows premiered in each decade."""

    def __init__(self):
        super().__init__("shows_per_decade")

    def compute(self, records):
        decade_counts = {}

        for show in records:
            if show.year is None:
                continue

            decade = (show.year // 10) * 10
            decade_name = f"{decade}s"

            decade_counts[decade_name] = (
                decade_counts.get(decade_name, 0) + 1
            )

        return decade_counts


class DataQuirks(Aggregation):
    """Summarize missing values and unique languages."""

    def __init__(self):
        super().__init__("data_quirks")

    def compute(self, records):
        shows_without_genres = 0
        shows_without_rating = 0
        shows_without_network = 0
        shows_without_premiered_date = 0
        unique_languages = set()

        for show in records:
            if not show.genres:
                shows_without_genres += 1

            if show.rating is None:
                shows_without_rating += 1

            if not show.has_network:
                shows_without_network += 1

            if not show.premiered:
                shows_without_premiered_date += 1

            if show.language:
                unique_languages.add(show.language)

        return {
            "shows_without_genres": shows_without_genres,
            "shows_without_rating": shows_without_rating,
            "shows_without_network": shows_without_network,
            "shows_without_premiered_date": shows_without_premiered_date,
            "unique_languages": sorted(unique_languages),
        }