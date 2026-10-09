# TV Summary

An installable Python package that downloads TV show records from TVMaze, summarizes them, and saves the results as JSON.   
It refactors the Lab 02 program into classes and modules while preserving its summary keys and calculations.

## Data source

URL: https://api.tvmaze.com/shows?page=0

Each record represents one TV show. The program uses its language, genres, average rating, network, and premiere date. The Show class also stores its name.

The Lab 02 run returned approximately 240 records. The source data may change over time.

## Setup

Install Anaconda or Miniconda and Git first.

Clone the repository and enter its folder:

```bash
git clone https://github.com/safi111287/lab03.git test-lab03-clone
```
```bash
cd test-lab03-clone
```

Create and activate the environment, install the pinned dependencies, and install the package:

```bash
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

The conda environment uses Python 3.11. The editable installation allows changes to the package code to be used without reinstalling it.

## Run

Run this command from the repository root:

```bash
python main.py
```

The program downloads the records, prints the summary, and saves it to:

```text
data/processed/summary.json
```
To view the generated summary on Windows:

```bash
notepad data\processed\summary.json
```

The output contains:

- Source URL and number of records processed.
- Number of shows per genre.
- Average rating by language.
- Number of shows per network.
- Number of shows per premiere decade.
- Missing-value counts and unique languages.

If downloading fails, the program prints a clear message and stops without a traceback. If writing the output fails, it prints a clear message.

## Test

Run the tests from the repository root:

```bash
python -m unittest discover -s tests
```

The three tests in `tests/test_models.py` exercise the Show class using handmade records. They cover valid records, missing values, and malformed values. They do not make network requests.

When finished, optionally deactivate the environment:

```bash
conda deactivate
```

## Layout

- `main.py`: Coordinates downloading, summary creation, and writing; handles download errors.
- `src/tvsummary/__init__.py`: Re-exports public classes and functions for direct package imports.
- `src/tvsummary/config.py`: Keeps the source URL, request timeout, and output path together.
- `src/tvsummary/models.py`: Defines Show and cleans each record when it is created.
- `src/tvsummary/sources.py`: Defines ShowSource and DownloadError; isolates downloading and is the only module that imports requests.
- `src/tvsummary/aggregations.py`: Defines the Aggregation base class and five calculation subclasses.
- `src/tvsummary/report.py`: Builds the summary and writes it to JSON, keeping reporting separate from downloading and calculations.
- `tests/test_models.py`: Contains offline tests for Show.
- `environment.yml`: Defines the conda environment name, Python version, and pip.
- `requirements.txt`: Pins the pip dependency versions.
- `pyproject.toml`: Defines package metadata, dependencies, and discovery under src.
- `.gitignore`: Excludes generated and private files.
- `data/raw/.gitkeep`: Preserves the empty raw-data folder in Git.
- `data/processed/summary.json`: Stores the output of a successful run.

## What moved where

| Lab 02 function or setting | Location in Lab 03 |
|---|---|
| `fetch_records(url)` | `sources.py`: `ShowSource.fetch_records()` |
| `shows_per_genre(records)` | `aggregations.py`: `ShowsPerGenre.compute()` |
| `average_rating_by_language(records)` | `aggregations.py`: `AverageRatingByLanguage.compute()` |
| `shows_per_network(records)` | `aggregations.py`: `ShowsPerNetwork.compute()` |
| `shows_per_decade(records)` | `aggregations.py`: `ShowsPerDecade.compute()` |
| `data_quirks(records)` | `aggregations.py`: `DataQuirks.compute()` |
| `build_summary(records)` | `report.py`: `build_summary()` |
| `write_summary(summary, path)` | `report.py`: `write_summary()` |
| `main()` | `main.py`: `main()` |
| Record-value checks inside calculation functions | `models.py`: `Show.__init__()` |
| `source_url`, request timeout, and output path | `config.py`: `SOURCE_URL`, `TIMEOUT`, and `OUTPUT_PATH` |

## Design choices

### Show

Show represents one TV show. Its constructor centralizes cleaning so that calculations can use attributes instead of repeatedly checking raw dictionaries.

Missing genres become an empty list. Missing or invalid ratings become None and are excluded from rating averages. Missing network names use "No Network". The year is extracted from the first four characters of the premiere date, matching the original calculation.

The `has_network` attribute separately tracks whether network information was present. This preserves the original distinction between missing network information and a network object without a name.

The `__str__` method returns the show name.

### ShowSource and DownloadError

ShowSource manages downloading and returns Show objects instead of raw dictionaries. Its URL and timeout default to the settings in config.py.

DownloadError carries download failures to main.py, where a readable message is printed. This keeps requests-specific error handling inside sources.py.

### Aggregation and inheritance

Aggregation provides a result key and a common compute method. Its five subclasses override compute:

- ShowsPerGenre
- AverageRatingByLanguage
- ShowsPerNetwork
- ShowsPerDecade
- DataQuirks

The summary builder loops over a mixed list of these objects and calls compute on each one without checking its subclass. Each object supplies its own calculation through the same interface.

To add another calculation, create an Aggregation subclass, set its result key, implement compute, and add an instance to the list in build_summary.

### Reporting and entry point

report.py separates summary assembly and JSON writing from downloading and individual calculations. main.py remains a short entry point that connects these responsibilities.

### Behaviour preservation

The original and refactored summary builders were compared using the same downloaded records. Their dictionaries matched, including all summary keys and values.

The original records.py was removed when the package replaced it. Its unchanged version remains available in the Git commit history.

## Known limitations

- Only TVMaze page 0 is downloaded; the program does not retrieve all API pages.
- Downloading requires an internet connection and an available TVMaze service.
- Source updates can change the output between runs.
- Raw records are held in memory and are not saved under data/raw.
- Premiere-year extraction checks the first four characters rather than validating the entire date.
- The program should be run from the repository root because the output path is relative.
- The current automated tests cover Show; the remaining modules do not yet have automated test coverage.