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
