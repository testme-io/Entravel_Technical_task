import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:3000")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"