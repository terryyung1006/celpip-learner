# CELPIP Learner Frame — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the monorepo frame — empty Next.js frontend, Python agent backend wired to claude-code-proxy, and Docker Compose for postgres + redis + proxy.

**Architecture:** Frontend (Next.js 14) and backend (Python + claude-agent-sdk) run locally. Three Docker services provide infrastructure: postgres for long-term memory, redis for short-term memory, and claude-code-proxy as the LLM routing layer. The backend points `ANTHROPIC_BASE_URL` at the local proxy so any LLM provider can be swapped via env var.

**Tech Stack:** Next.js 14, TypeScript, Tailwind CSS, Python 3.12, uv, claude-agent-sdk, psycopg2-binary, redis-py, python-dotenv, pytest, Docker Compose, postgres:16, redis:7, ghcr.io/1rgs/claude-code-proxy:latest

---

## File Map

| File | Purpose |
|------|---------|
| `backend/pyproject.toml` | Python project config + uv dependencies |
| `backend/.python-version` | Pin Python 3.12 for uv |
| `backend/agent/__init__.py` | Agent frame: env loading + runnable entry point |
| `backend/tests/__init__.py` | Test package marker |
| `backend/tests/test_agent.py` | Smoke tests: imports + async shape |
| `frontend/` | Next.js 14 scaffold (create-next-app) |
| `proxy/config.yaml` | Documents proxy model-routing env vars |
| `docker-compose.yml` | postgres + redis + proxy services |
| `.env.example` | All required env vars with descriptions |
| `README.md` | Setup instructions for new contributors |

---

## Task 1: Backend — project config

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/.python-version`

- [ ] **Step 1: Create `backend/.python-version`**

```
3.12
```

- [ ] **Step 2: Create `backend/pyproject.toml`**

```toml
[project]
name = "celpip-backend"
version = "0.1.0"
description = "CELPIP writing practice AI agent"
requires-python = ">=3.12"
dependencies = [
    "claude-agent-sdk",
    "psycopg2-binary>=2.9",
    "redis>=5.0",
    "python-dotenv>=1.0",
    "anyio>=4.0",
]

[project.scripts]
celpip-agent = "agent:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["agent"]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 3: Install dependencies and verify**

```bash
cd backend
uv sync --all-groups
```

Expected: uv creates `.venv/` and `uv.lock`, no errors.

- [ ] **Step 4: Commit**

```bash
git add backend/pyproject.toml backend/.python-version backend/uv.lock
git commit -m "feat: add backend Python project config"
```

---

## Task 2: Backend — agent frame + smoke tests

**Files:**
- Create: `backend/agent/__init__.py`
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/test_agent.py`

- [ ] **Step 1: Create `backend/tests/__init__.py`** (empty file)

- [ ] **Step 2: Write the failing test — create `backend/tests/test_agent.py`**

```python
import inspect
import pytest


def test_run_agent_is_importable():
    from agent import run_agent
    assert callable(run_agent)


def test_run_agent_is_async():
    from agent import run_agent
    assert inspect.iscoroutinefunction(run_agent)


def test_main_is_importable():
    from agent import main
    assert callable(main)
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd backend
uv run pytest tests/test_agent.py -v
```

Expected: `ImportError` or `ModuleNotFoundError` — `agent` module not found yet.

- [ ] **Step 4: Create `backend/agent/__init__.py`**

```python
import os
import anyio
from dotenv import load_dotenv
from claude_agent_sdk import query

load_dotenv()

DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
REDIS_URL: str = os.environ.get("REDIS_URL", "")
# ANTHROPIC_API_KEY and ANTHROPIC_BASE_URL are read by claude-agent-sdk from env


async def run_agent(prompt: str) -> list[str]:
    responses: list[str] = []
    async for message in query(prompt=prompt):
        responses.append(str(message))
    return responses


def main() -> None:
    anyio.run(run_agent, "Hello from CELPIP agent")
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd backend
uv run pytest tests/test_agent.py -v
```

Expected:
```
PASSED tests/test_agent.py::test_run_agent_is_importable
PASSED tests/test_agent.py::test_run_agent_is_async
PASSED tests/test_agent.py::test_main_is_importable
3 passed
```

- [ ] **Step 6: Commit**

```bash
git add backend/agent/__init__.py backend/tests/__init__.py backend/tests/test_agent.py
git commit -m "feat: add backend agent frame with smoke tests"
```

---

## Task 3: Frontend scaffold

**Files:**
- Create: `frontend/` (via create-next-app)

- [ ] **Step 1: Scaffold Next.js 14 app**

Run from the repo root:

```bash
npx create-next-app@14 frontend \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*" \
  --eslint
```

- [ ] **Step 2: Verify dev server starts**

```bash
cd frontend
npm run dev
```

Expected: Server starts on `http://localhost:3000`, default Next.js page loads in browser. Stop with `Ctrl+C`.

- [ ] **Step 3: Commit**

```bash
git add frontend/
git commit -m "feat: add empty Next.js 14 frontend scaffold"
```

---

## Task 4: Proxy config

**Files:**
- Create: `proxy/config.yaml`

- [ ] **Step 1: Create `proxy/config.yaml`**

```yaml
# claude-code-proxy model routing configuration
# Reference: https://github.com/1rgs/claude-code-proxy
#
# Configure via environment variables in .env (picked up by docker-compose).
# The proxy exposes a Claude-compatible API on port 8082.
# Backend connects via: ANTHROPIC_BASE_URL=http://localhost:8082
#
# Required env vars (set at least one provider):
#
#   PREFERRED_PROVIDER=anthropic|openai|google
#
#   # Anthropic
#   ANTHROPIC_API_KEY=sk-ant-...
#
#   # OpenAI
#   OPENAI_API_KEY=sk-...
#
#   # Google Vertex AI
#   GEMINI_API_KEY=...
#   USE_VERTEX_AUTH=true        # optional, for service account auth
#   VERTEX_PROJECT=my-project
#   VERTEX_LOCATION=us-central1
#
# Optional model overrides:
#   BIG_MODEL=claude-opus-4-5       # or gpt-4o, gemini-2.0-flash-exp, etc.
#   SMALL_MODEL=claude-haiku-4-5-20251001  # or gpt-4o-mini, etc.
#
# Example: route everything through OpenAI
#   PREFERRED_PROVIDER=openai
#   OPENAI_API_KEY=sk-...
#   BIG_MODEL=gpt-4o
#   SMALL_MODEL=gpt-4o-mini
```

- [ ] **Step 2: Commit**

```bash
git add proxy/config.yaml
git commit -m "feat: add proxy model routing config docs"
```

---

## Task 5: Docker Compose + environment config

**Files:**
- Create: `docker-compose.yml`
- Create: `.env.example`

- [ ] **Step 1: Create `docker-compose.yml`**

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: celpip
      POSTGRES_PASSWORD: celpip
      POSTGRES_DB: celpip
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U celpip"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  proxy:
    image: ghcr.io/1rgs/claude-code-proxy:latest
    ports:
      - "8082:8082"
    env_file:
      - .env

volumes:
  postgres_data:
```

- [ ] **Step 2: Create `.env.example`**

```bash
# ── LLM ───────────────────────────────────────────────────────────────────────
# Backend connects to the proxy; proxy routes to the actual LLM provider.
ANTHROPIC_BASE_URL=http://localhost:8082

# ── Proxy routing ─────────────────────────────────────────────────────────────
# Set PREFERRED_PROVIDER and the matching API key.
PREFERRED_PROVIDER=anthropic

ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GEMINI_API_KEY=

# Optional: override which models the proxy uses
BIG_MODEL=claude-opus-4-5
SMALL_MODEL=claude-haiku-4-5-20251001

# ── Database (matches docker-compose defaults) ─────────────────────────────────
DATABASE_URL=postgresql://celpip:celpip@localhost:5432/celpip

# ── Redis (matches docker-compose defaults) ────────────────────────────────────
REDIS_URL=redis://localhost:6379
```

- [ ] **Step 3: Copy `.env.example` to `.env` and add your API key, then bring services up**

```bash
cp .env.example .env
# Edit .env: set ANTHROPIC_API_KEY (or whichever provider you're using)
docker compose up -d
```

- [ ] **Step 4: Verify all three services are healthy**

```bash
docker compose ps
```

Expected: `postgres`, `redis`, and `proxy` all show `healthy` or `running`.

```bash
docker compose logs proxy --tail 20
```

Expected: proxy starts without errors, logs indicate it's listening on port 8082.

- [ ] **Step 5: Add `.env` to `.gitignore`**

Append to `.gitignore` (create it if it doesn't exist):

```
.env
backend/.venv/
__pycache__/
*.pyc
.DS_Store
```

- [ ] **Step 6: Commit**

```bash
git add docker-compose.yml .env.example .gitignore
git commit -m "feat: add docker-compose with postgres, redis, and proxy"
```

---

## Task 6: README

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace `README.md` with setup instructions**

```markdown
# celpip-learner

A web app for practicing the CELPIP Writing test, powered by an AI agent.

## Prerequisites

- [Node.js 20+](https://nodejs.org)
- [Python 3.12](https://python.org)
- [uv](https://docs.astral.sh/uv/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Quick Start

**1. Environment setup**

```bash
cp .env.example .env
# Edit .env and set your API key (ANTHROPIC_API_KEY or OPENAI_API_KEY etc.)
```

**2. Start infrastructure (proxy + postgres + redis)**

```bash
docker compose up -d
```

**3. Start backend agent**

```bash
cd backend
uv sync --all-groups
uv run celpip-agent
```

**4. Start frontend**

```bash
cd frontend
npm install
npm run dev
```

Frontend → http://localhost:3000  
Backend agent → runs as a process (HTTP server added in next phase)  
Proxy (LLM routing) → http://localhost:8082  

## Switching LLM Providers

Edit `.env`:

```bash
# Use OpenAI instead of Anthropic
PREFERRED_PROVIDER=openai
OPENAI_API_KEY=sk-...
BIG_MODEL=gpt-4o
SMALL_MODEL=gpt-4o-mini
```

Then restart the proxy: `docker compose restart proxy`

## Project Structure

```
celpip-learner/
├── frontend/          # Next.js 14 app (npm run dev)
├── backend/           # Python AI agent (uv run celpip-agent)
├── proxy/             # claude-code-proxy config docs
├── docker-compose.yml # postgres + redis + proxy
└── .env.example       # environment variable template
```
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add setup instructions to README"
```

---

## Done

At this point the repo has:
- `frontend/` — runnable Next.js 14 scaffold
- `backend/` — importable Python agent frame wired to the proxy, with passing smoke tests
- `docker-compose.yml` — one command brings up postgres, redis, and the LLM proxy
- `.env.example` — all config documented
- `README.md` — contributor onboarding instructions
