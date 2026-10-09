"""Package for summarizing TV show data."""

from .models import Show
from .sources import ShowSource, DownloadError
from .aggregations import (
    Aggregation,
    ShowsPerGenre,
    AverageRatingByLanguage,
    ShowsPerNetwork,
    ShowsPerDecade,
    DataQuirks,
)
from .report import build_summary, write_summary