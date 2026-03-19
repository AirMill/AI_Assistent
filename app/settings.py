from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


DEFAULT_ENV_TEMPLATE = '''# =========================
# Coachable AI Assistant
# Auto-created starter config
# Fill in your real API key and restart the app
# =========================

OPENAI_API_KEY=
OPENAI_CHAT_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
TOP_K=5
KNOWLEDGE_DIR=data/books
INDEX_PATH=data/index/index.json
SYSTEM_PRINCIPLES_PATH=data/books/principles.md
AUTO_INGEST_ON_STARTUP=true
SUPPORTED_EXTENSIONS=.md,.txt,.pdf,.docx
'''


def ensure_env_file() -> None:
    env_path = Path(".env")
    if not env_path.exists():
        env_path.write_text(DEFAULT_ENV_TEMPLATE, encoding="utf-8")


class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    top_k: int = 5
    knowledge_dir: str = "data/books"
    index_path: str = "data/index/index.json"
    system_principles_path: str = "data/books/principles.md"
    auto_ingest_on_startup: bool = True
    supported_extensions: str = ".md,.txt,.pdf,.docx"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    ensure_env_file()
    return Settings()
