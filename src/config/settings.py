import os
from functools import lru_cache


class Settings:
    """Application settings"""

    def __init__(self):
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.api_port: int = int(os.getenv("API_PORT", "8000"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.max_transcript_length: int = int(os.getenv("MAX_TRANSCRIPT_LENGTH", "50000"))


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
