# Coachable AI Assistant

Drop your books into `data/books/` and run — no setup required.

This is a GitHub-ready starter kit for a practical AI assistant that can answer using your own notes, PDFs, Word files, and principles. It is designed to be easy to share with friends: they can clone the repo, add files, run it, and start asking questions.

## What this project does

The app automatically:

- scans `data/books/`
- finds supported files
- extracts text from them
- chunks and embeds the content
- answers questions using the most relevant material first

Supported file types by default:

- `.pdf`
- `.docx`
- `.md`
- `.txt`

This is **not** model fine-tuning. It is a retrieval-based assistant, which means it uses your documents as a searchable knowledge base.

## Zero-config behavior

This version is built to run even when no `.env` file exists.

Behavior:

- if `.env` exists, the app uses it
- if `.env` does not exist, the app auto-creates one with starter values
- if no OpenAI API key is set, the server still starts
- health checks still work
- chat and indexing endpoints return a clear setup message until a real API key is added

That means your friends can start the project without wrestling with config first.

## Folder structure

```text
.
├── app/
│   ├── knowledge.py
│   ├── main.py
│   └── settings.py
├── data/
│   ├── books/
│   │   ├── principles.md
│   │   ├── example_notes.md
│   │   ├── put_books_here.txt
│   │   └── your_files_go_here.pdf / .docx / .md / .txt
│   └── index/
├── scripts/
│   └── ingest.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Quick start

### Option A — fastest path

1. Clone the repo.
2. Put your files into `data/books/`.
3. Start the app:
   ```bash
   docker compose up --build
   ```
4. Open the generated `.env` and paste your OpenAI key.
5. Restart the app:
   ```bash
   docker compose up --build
   ```

### Option B — configure first

1. Clone the repo.
2. Copy the example config:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and set `OPENAI_API_KEY`.
4. Put your files into `data/books/`.
5. Start the app:
   ```bash
   docker compose up --build
   ```

## Tutorial: how to use it

### 1) Add your books and notes

Put files into:

```text
data/books/
```

Good inputs include:

- your own book summaries
- frameworks
- how-to notes
- playbooks
- decision rules
- case studies
- operating principles

Notes:

- `.docx` is supported
- old `.doc` files are not included in this starter
- text PDFs work best
- scanned image PDFs may extract poorly without OCR

### 2) Add your logic

Use `data/books/principles.md` to teach the assistant how you want it to reason.

A strong `principles.md` usually contains:

- how to diagnose problems
- how to prioritize
- what tradeoffs matter
- what “good” looks like
- your preferred step-by-step approach

This is the best place to put the “logic” you want to teach it.

### 3) Start the app

```bash
docker compose up --build
```

The server will start on:

```text
http://localhost:8000
```

### 4) Check health

```bash
curl http://localhost:8000/health
```

You should get JSON showing status, indexed chunk count, and supported extensions.

### 5) Ask a question

```bash
curl -X POST http://localhost:8000/chat   -H "Content-Type: application/json"   -d '{"message":"What principles should I use to solve recurring operational problems?"}'
```

### 6) Rebuild or refresh the knowledge index

Force a full rebuild:

```bash
curl -X POST http://localhost:8000/ingest
```

Refresh only if files changed:

```bash
curl -X POST http://localhost:8000/refresh
```

### 7) Add more files later

Just drop more supported files into `data/books/` and call:

```bash
curl -X POST http://localhost:8000/refresh
```

## API endpoints

### `GET /health`

Shows whether the server is up and whether an API key is configured.

### `POST /chat`

Ask the assistant a question.

Example body:

```json
{
  "message": "Give me a practical plan for fixing a recurring team bottleneck.",
  "use_knowledge": true
}
```

### `POST /ingest`

Forces a full index rebuild from `data/books/`.

### `POST /refresh`

Only rebuilds if files have changed.

## Recommended way to teach it

Best results usually come from your own distilled notes rather than giant raw dumps.

A strong pattern is:

- `principles.md` for reasoning style
- one file per topic
- concise summaries from books
- examples of decisions and why they worked
- step-by-step methods you want repeated

## Example workflow

You read a business or psychology book and then create a note like this:

- `how_to_handle_conflict.md`
- `decision_frameworks.md`
- `leadership_principles.docx`
- `systems_thinking.pdf`

The assistant will search those files and use them to answer in a way that reflects your material.

## Running without Docker

You can also run it locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Sharing it on GitHub

Recommended setup:

1. commit the code
2. do not commit `.env`
3. do not commit private books or notes
4. keep only the example files in `data/books/`
5. let each person add their own files locally

The included `.gitignore` already keeps most personal content out of Git.

## Important limits

- scanned-image PDFs are not OCRed in this version
- `.doc` files are not supported by default
- very large libraries may eventually need a vector database
- raw copyrighted books should not be published in a public repo

## Troubleshooting

### The server starts but chat says the API key is missing

That means `.env` exists but `OPENAI_API_KEY` is empty. Add your key and restart.

### I added files but answers do not mention them

Call:

```bash
curl -X POST http://localhost:8000/refresh
```

### A PDF does not extract well

It may be a scanned PDF with no selectable text. Convert it with OCR first or replace it with your own notes.

## Easy next upgrades

- OCR for scanned PDFs
- browser chat UI
- Telegram or Discord bot
- authentication
- vector database for larger libraries

## License and usage

Use this starter as a base project for yourself or your friends. Replace the example notes with your own material and build on top of it.
