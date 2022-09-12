import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_DIR = Path(__file__).resolve().parent
    PORT = os.getenv('SOCKET_PORT', default='9999')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
