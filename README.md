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
- uploads still work
- chat and indexing endpoints return a clear setup message until a real API key is added

That means your friends can start the project without wrestling with config first.

## Folder structure

```text
.
├── app/
│   ├── knowledge.py
│   ├── main.py
│   ├── settings.py
│   └── static/
│       └── index.html
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
2. Start the app:
   ```bash
   docker compose up --build
   ```
3. Open `http://localhost:8000`
4. Drag and drop files into the upload panel.
5. Open the generated `.env` and paste your OpenAI key.
6. Restart the app:
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
4. Start the app:
   ```bash
   docker compose up --build
   ```
5. Open `http://localhost:8000`
6. Drag and drop files into the upload panel or put them in `data/books/`.

## Tutorial: how to use it

### 1) Start the app

```bash
docker compose up --build
```

The server will start on:

```text
http://localhost:8000
```

Open that address in your browser to use the built-in chat UI.

### 2) Add your books and notes

You now have two ways to add material:

#### A. Drag and drop in the browser UI

Open:

```text
http://localhost:8000
```

Then drag `.pdf`, `.docx`, `.md`, or `.txt` files into the upload area and click **Upload files**.

The app will save them into:

```text
data/books/
```

If your API key is already configured, the app will also refresh the knowledge index automatically.

#### B. Copy files into the folder manually

Put files into:

```text
data/books/
```

Then click **Refresh books** in the UI, or call:

```bash
curl -X POST http://localhost:8000/refresh
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

### 3) Add your logic

Use `data/books/principles.md` to teach the assistant how you want it to reason.

A strong `principles.md` usually contains:

- how to diagnose problems
- how to prioritize
- what tradeoffs matter
- what “good” looks like
- your preferred step-by-step approach

This is the best place to put the “logic” you want to teach it.

### 4) Open the UI

Go to:

```text
http://localhost:8000
```

From the UI you can:

- see whether your API key is configured
- see how many chunks are indexed
- upload files with drag and drop
- click **Refresh books** after adding files
- click **Full rebuild** to force a new index
- chat with your assistant in the browser

### 5) Check health manually (optional)

```bash
curl http://localhost:8000/health
```

### 6) Ask a question by API (optional)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What principles should I use to solve recurring operational problems?"}'
```

### 7) Upload files by API (optional)

```bash
curl -X POST http://localhost:8000/upload \
  -F "files=@./some-book.pdf" \
  -F "files=@./notes.docx"
```

### 8) Rebuild or refresh the knowledge index

Force a full rebuild:

```bash
curl -X POST http://localhost:8000/ingest
```

Refresh only if files changed:

```bash
curl -X POST http://localhost:8000/refresh
```

## GitHub sharing tips

Commit these files:

- app code
- Dockerfile
- docker-compose.yml
- `.env.example`
- README
- sample files

Do **not** commit:

- `.env`
- `data/index/`
- personal API keys

Recommended `.gitignore` entries:

```gitignore
.env
data/index/
__pycache__/
*.pyc
```

## Typical workflow

1. Start the app.
2. Drop books or notes into the UI.
3. Add or refine `principles.md`.
4. Refresh books.
5. Ask questions.
6. Keep improving your notes over time.

## Troubleshooting

### The server runs but chat says API key is missing

That means the app started in zero-config mode. Add your real key to `.env` and restart.

### Upload works but indexing does not happen

Same root cause: upload does not require a key, but embedding and chat do.

### My PDF gives weak answers

It may be an image-only PDF. This starter extracts text from text PDFs, not scanned images with OCR.

### Port 8000 is busy

Change the port mapping in `docker-compose.yml`.

## License / usage note

If you share this publicly, it is safer to upload your own notes and summaries than raw copyrighted books.
