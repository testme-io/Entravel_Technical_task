import logging
import requests
from config.settings import API_TIMEOUT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.timeout = API_TIMEOUT

    def get(self, url, **kwargs):
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        logger.info("GET %s -> %s", url, response.status_code)
        return response

    def post(self, url, payload=None, **kwargs):
        response = self.session.post(url, json=payload, timeout=self.timeout, **kwargs)
        logger.info("POST %s | payload: %s -> %s", url, payload, response.status_code)
        return response

    def delete(self, url, **kwargs):
        response = self.session.delete(url, timeout=self.timeout, **kwargs)
        logger.info("DELETE %s -> %s", url, response.status_code)
        return response