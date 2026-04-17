import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Holds runtime configuration loaded from environment variables."""

    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.api_key = os.getenv("API_KEY", "guest-demo-key").strip()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "5"))
        self.search_results = int(os.getenv("SEARCH_RESULTS", "8"))
        self.request_timeout = float(os.getenv("REQUEST_TIMEOUT", "30"))


settings = Settings()
