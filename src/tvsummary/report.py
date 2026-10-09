import json

from .config import SOURCE_URL, OUTPUT_PATH
from .aggregations import (
    ShowsPerGenre,
    AverageRatingByLanguage,
    ShowsPerNetwork,
    ShowsPerDecade,
    DataQuirks,
)


def build_summary(records):
    """Combine all aggregations into one summary."""
    summary = {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
    }

    aggregations = [
        ShowsPerGenre(),
        AverageRatingByLanguage(),
        ShowsPerNetwork(),
        ShowsPerDecade(),
        DataQuirks(),
    ]

    for aggregation in aggregations:
        summary[aggregation.key] = aggregation.compute(records)

    return summary


def write_summary(summary, path=OUTPUT_PATH):
    """Write the summary to a JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2)

    except OSError as error:
        print(f"Could not write summary to {path}: {error}")
        return False

    return True