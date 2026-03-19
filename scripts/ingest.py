from openai import OpenAI

from app.knowledge import KnowledgeBase
from app.settings import get_settings


def get_extensions(raw: str) -> set[str]:
    return {ext.strip().lower() for ext in raw.split(",") if ext.strip()}


def main() -> None:
    settings = get_settings()
    if not settings.openai_api_key.strip():
        raise SystemExit("OPENAI_API_KEY is not configured. Add it to .env before running ingest.")

    client = OpenAI(api_key=settings.openai_api_key)
    kb = KnowledgeBase(settings.index_path, client, settings.openai_embedding_model)
    result = kb.build_from_directory(settings.knowledge_dir, get_extensions(settings.supported_extensions))
    print(result)


if __name__ == "__main__":
    main()
