# CELPIP Learner — Frame Design

**Date:** 2026-04-25  
**Scope:** Repository skeleton only. No agent business logic, no frontend pages — just the structural frame to build on.

---

## Goal

Establish a monorepo that wires together:
- An empty Next.js frontend (to be designed later)
- A Python AI agent backend using `claude-agent-sdk-python`
- `claude-code-proxy` for LLM model flexibility
- PostgreSQL (long-term memory) and Redis (short-term memory) as infrastructure

Frontend and backend run locally in dev. Only the proxy and data services run in Docker.

---

## Repository Layout

```
celpip-learner/
├── frontend/                  # Next.js 14 app — runs locally
│   ├── app/
│   ├── public/
│   └── package.json
│
├── backend/                   # Python agent — runs locally
│   ├── agent/
│   │   └── __init__.py        # Agent entry point (empty frame)
│   └── pyproject.toml
│
├── proxy/                     # claude-code-proxy config
│   └── config.yaml            # Model routing rules
│
├── docker-compose.yml         # postgres + redis + proxy
├── .env.example               # All required env vars documented
└── README.md
```

---

## Frontend

- **Framework:** Next.js 14, App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Package manager:** npm
- **State:** Empty scaffold — default `create-next-app` output, no custom pages yet
- **Dev:** `npm run dev` (runs locally, not in Docker)

---

## Backend

- **Language:** Python 3.12
- **Package manager:** uv
- **Key dependencies:** `anthropic`, `claude-agent-sdk`, `psycopg2-binary`, `redis`
- **Entry point:** `backend/agent/__init__.py` — instantiates agent, reads env vars for proxy URL, postgres, and redis connections
- **LLM routing:** All calls go through `ANTHROPIC_BASE_URL` (pointing at the local proxy)
- **Dev:** `uv run` (runs locally, not in Docker)
- **Business logic:** None at this stage — agent frame only

---

## Docker Compose Services

| Service    | Image            | Port  | Purpose                        |
|------------|------------------|-------|--------------------------------|
| `postgres` | `postgres:16`    | 5432  | Long-term memory (sessions, history) |
| `redis`    | `redis:7`        | 6379  | Short-term memory (active session state) |
| `proxy`    | `1rgs/claude-code-proxy` (pre-built) | 8082 | LLM model routing layer |

All services configured via environment variables from `.env`.

---

## Environment Variables

```
# LLM
ANTHROPIC_API_KEY=
ANTHROPIC_BASE_URL=http://localhost:8082

# Database
DATABASE_URL=postgresql://celpip:celpip@localhost:5432/celpip

# Redis
REDIS_URL=redis://localhost:6379

# Optional: alternate model providers (passed to proxy)
OPENAI_API_KEY=
```

---

## Data Flow (Frame)

```
User (browser)
  → Next.js frontend (localhost:3000)
  → Python backend agent (localhost:8000)
  → claude-code-proxy (localhost:8082)
  → LLM provider (Anthropic / OpenAI / etc.)

Agent also reads/writes:
  → PostgreSQL (long-term memory)
  → Redis (short-term memory)
```

---

## Out of Scope (This Phase)

- Agent tools, system prompt, or business logic
- Frontend pages or UI components
- Authentication
- Production deployment / Dockerfiles for frontend and backend
- Database schema migrations
