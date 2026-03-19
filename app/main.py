from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

from app.knowledge import KnowledgeBase
from app.settings import get_settings

settings = get_settings()


def get_client() -> OpenAI | None:
    if not settings.openai_api_key.strip():
        return None
    return OpenAI(api_key=settings.openai_api_key)


client = get_client()
kb = KnowledgeBase(settings.index_path, client, settings.openai_embedding_model) if client else None


def get_extensions() -> set[str]:
    return {ext.strip().lower() for ext in settings.supported_extensions.split(",") if ext.strip()}


def ensure_directories() -> None:
    Path(settings.knowledge_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.index_path).parent.mkdir(parents=True, exist_ok=True)


def require_client() -> OpenAI:
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is not configured. Add OPENAI_API_KEY to .env and restart the app.",
        )
    return client


def require_kb() -> KnowledgeBase:
    if kb is None:
        raise HTTPException(
            status_code=503,
            detail="Knowledge base is unavailable because OPENAI_API_KEY is not configured yet.",
        )
    return kb


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    if settings.auto_ingest_on_startup and client is not None:
        require_kb().ensure_index(settings.knowledge_dir, get_extensions())
    yield


app = FastAPI(title="Coachable AI Assistant", version="1.2.0", lifespan=lifespan)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    use_knowledge: bool = True


class IngestResponse(BaseModel):
    files_indexed: int
    chunks_indexed: int
    index_path: str
    skipped_files: list[str] = []
    rebuilt: bool | None = None


def read_principles() -> str:
    path = Path(settings.system_principles_path)
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "api_key_configured": bool(settings.openai_api_key.strip()),
        "indexed_chunks": len(require_kb().chunks) if kb is not None else 0,
        "knowledge_dir": settings.knowledge_dir,
        "supported_extensions": sorted(get_extensions()),
        "auto_ingest_on_startup": settings.auto_ingest_on_startup,
    }


@app.post("/ingest", response_model=IngestResponse)
def ingest() -> dict[str, Any]:
    kb_instance = require_kb()
    try:
        return kb_instance.build_from_directory(settings.knowledge_dir, get_extensions())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ingest failed: {exc}") from exc


@app.post("/refresh", response_model=IngestResponse)
def refresh() -> dict[str, Any]:
    kb_instance = require_kb()
    try:
        return kb_instance.ensure_index(settings.knowledge_dir, get_extensions())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {exc}") from exc


@app.post("/chat")
def chat(req: ChatRequest) -> dict[str, Any]:
    client_instance = require_client()
    kb_instance = require_kb()

    if settings.auto_ingest_on_startup:
        kb_instance.ensure_index(settings.knowledge_dir, get_extensions())

    context = []
    if req.use_knowledge:
        context = kb_instance.search(req.message, top_k=settings.top_k)

    principles = read_principles()
    context_block = "\n\n".join(
        [f"Source: {item['source']}\nScore: {item['score']}\n{item['text']}" for item in context]
    )

    system_prompt = f"""
You are a practical remote AI assistant trained by the repository owner.

Follow these rules:
1. Prefer the owner's written principles and book notes over generic advice.
2. If the knowledge base is relevant, answer from it and explicitly say what logic or principle you used.
3. If the answer is not in the supplied material, say so plainly and then give your best general answer.
4. Do not invent facts from books that are not in context.
5. Keep answers helpful, concrete, and easy to act on.

Owner principles:
{principles or 'No custom principles provided yet.'}

Retrieved knowledge:
{context_block or 'No relevant indexed knowledge was found.'}
""".strip()

    response = client_instance.responses.create(
        model=settings.openai_chat_model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": req.message},
        ],
    )

    return {
        "reply": response.output_text,
        "sources": [{"source": item["source"], "score": item["score"]} for item in context],
    }
