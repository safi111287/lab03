import requests

from .config import SOURCE_URL, TIMEOUT
from .models import Show


class DownloadError(Exception):
    """Indicate that TV show data could not be downloaded."""


class ShowSource:
    """Download TVMaze records and return Show objects."""

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        self.url = url
        self.timeout = timeout

    def fetch_records(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            records = response.json()
        except (requests.RequestException, ValueError) as error:
            raise DownloadError(str(error)) from None

        return [Show(record) for record in records]