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