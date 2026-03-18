import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger("pokeapi")

POKEAPI_BASE = "https://pokeapi.co/api/v2"


class PokeAPIClient:
    def __init__(self, base_url=POKEAPI_BASE, timeout=10.0, max_retries=3):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        retry = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

    def fetch(self, endpoint, name_or_id):
        url = f"{self.base_url}/{endpoint}/{name_or_id}"
        try:
            response = self._session.get(url, timeout=self.timeout)
        except requests.RequestException:
            logger.exception("Network error fetching %s", url)
            return None

        if response.status_code != 200:
            logger.warning("PokeAPI %s returned %d", url, response.status_code)
            return None

        logger.info("PokeAPI fetch: %s/%s", endpoint, name_or_id)
        return response.json()


default_client = PokeAPIClient()
