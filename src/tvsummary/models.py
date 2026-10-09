class Show:
    """Represent one TV show and clean its values."""

    def __init__(self, record):
        self.name = record.get("name") or "Unknown"

        language = record.get("language")
        self.language = language if isinstance(language, str) else None

        genres = record.get("genres")
        self.genres = (
            [genre for genre in genres if isinstance(genre, str)]
            if isinstance(genres, list)
            else []
        )

        rating_data = record.get("rating")
        if not isinstance(rating_data, dict):
            rating_data = {}

        rating = rating_data.get("average")
        try:
            self.rating = float(rating) if rating is not None else None
        except (TypeError, ValueError):
            self.rating = None

        network = record.get("network")
        self.has_network = bool(network)

        if isinstance(network, dict) and network.get("name"):
            self.network_name = network["name"]
        else:
            self.network_name = "No Network"

        premiered = record.get("premiered")
        self.premiered = (
            premiered if isinstance(premiered, str) else None
        )

        self.year = None
        if self.premiered and len(self.premiered) >= 4:
            year_text = self.premiered[:4]
            if year_text.isdigit():
                self.year = int(year_text)

    def __str__(self):
        return self.name