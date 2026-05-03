# CELPIP Learner

A web app for practicing the CELPIP Writing test, powered by an AI agent.

## Pain Points This Project Solves

Existing online CELPIP writing practice tools have these problems:

1. **Inconsistent LLM evaluation** — LLMs score the same writing differently across sessions. Without a structured, repeatable evaluation method, feedback is unreliable and can't be trusted for improvement tracking.

2. **Feedback loop is too long** — Practicing a full writing passage (Task 1: email, Task 2: essay) and waiting for holistic feedback is slow. Users need faster, targeted feedback cycles.

3. **Can't practice by individual criteria** — The CELPIP writing rubric has four criteria: Coherence, Vocabulary, Readability, and Spelling & Punctuation. No tool lets you isolate and drill a specific criterion.

4. **Limited sample questions** — Existing tools have a fixed bank of practice prompts. With LLMs, there is no reason to ever run out of varied, realistic practice questions.

## Project Structure

```
celpip-learner/
├── frontend/          # Next.js 14 app (npm run dev → localhost:3000)
├── backend/           # Python AI agent (uv run celpip-agent)
├── proxy/             # claude-code-proxy config (model routing docs)
├── docker-compose.yml # postgres + redis + proxy (docker compose up -d)
└── .env.example       # environment variable template
```

## Architecture

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, App Router
- **Backend**: Python 3.12, `claude-agent-sdk`, managed with `uv`
- **LLM routing**: `claude-code-proxy` on port 8082 — swap providers via `PREFERRED_PROVIDER` in `.env`
- **Long-term memory**: PostgreSQL (sessions, history, progress)
- **Short-term memory**: Redis (active session state)

## Local Dev Setup

```bash
cp .env.example .env          # then fill in your API key
docker compose up -d           # starts postgres, redis, proxy
cd backend && uv sync --all-groups && uv run celpip-agent
cd frontend && npm install && npm run dev
```

## Key Decisions

- LLM calls go through the proxy, never directly to providers — keeps model switching a one-line config change
- Frontend and backend run locally in dev (not containerised) for fast iteration
- PostgreSQL for anything that needs to persist across sessions; Redis for in-flight session state only
