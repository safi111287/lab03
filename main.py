from tvsummary import ShowSource, DownloadError, build_summary, write_summary
from tvsummary.config import OUTPUT_PATH


def main():
    """Download TV shows, build the summary, and save it."""
    source = ShowSource()

    try:
        records = source.fetch_records()
    except DownloadError as error:
        print(f"Could not download TV show data: {error}")
        return

    summary = build_summary(records)

    print(f"\nDownloaded {len(records)} records from {source.url}")
    print(f"\nSummary of TV show data: {summary}")

    if write_summary(summary):
        print(f"\nSummary written to {OUTPUT_PATH}\n")


if __name__ == "__main__":
    main()