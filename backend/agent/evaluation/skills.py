import json
from claude_agent_sdk import query
from claude_agent_sdk.types import AssistantMessage, TextBlock
from agent.evaluation.models import EvaluationResult, ReferenceExample, Criterion
from agent.evaluation.rubrics import (
    COHERENCE_RUBRIC,
    VOCABULARY_RUBRIC,
    READABILITY_RUBRIC,
    TASK_FULFILMENT_RUBRIC,
)
from agent.evaluation.reference_examples import REFERENCE_EXAMPLES


def _build_prompt(
    criterion: Criterion,
    rubric: str,
    reference_examples: list[ReferenceExample],
    text: str,
) -> str:
    examples_block = "\n\n".join(
        f"[Band {ex.band_score} — {ex.task_type}]:\n{ex.text}"
        for ex in reference_examples
    )
    criterion_label = criterion.replace("_", " ").title()
    return (
        f"You are a CELPIP writing evaluator. Evaluate the following writing against the "
        f"{criterion_label} criterion.\n\n"
        f"RUBRIC:\n{rubric}\n\n"
        f"CALIBRATION EXAMPLES (real CELPIP responses with known band scores):\n{examples_block}\n\n"
        f"WRITING TO EVALUATE:\n{text}\n\n"
        f"Respond with ONLY a JSON object (no other text):\n"
        '{"band_score": <integer 1-12>, "feedback": "<2-3 sentences explaining the score>"}'
    )


async def _evaluate(
    criterion: Criterion,
    rubric: str,
    reference_examples: list[ReferenceExample],
    text: str,
) -> EvaluationResult:
    prompt = _build_prompt(criterion, rubric, reference_examples, text)
    parts: list[str] = []
    async for message in query(prompt=prompt):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    parts.append(block.text)
    raw = "".join(parts)
    if not raw.strip():
        raise ValueError("LLM returned an empty response")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {raw!r}") from e
    try:
        raw_score = data["band_score"]
        feedback = data["feedback"]
    except (KeyError, TypeError) as e:
        raise ValueError(f"LLM response missing expected fields: {data!r}") from e
    if not isinstance(raw_score, int) or isinstance(raw_score, bool):
        raise ValueError(f"band_score must be an integer, got {raw_score!r}")
    if not 1 <= raw_score <= 12:
        raise ValueError(f"band_score {raw_score} out of range 1-12")
    return EvaluationResult(criterion=criterion, band_score=raw_score, feedback=feedback)


async def evaluate_coherence(
    text: str,
    reference_examples: list[ReferenceExample] | None = None,
) -> EvaluationResult:
    return await _evaluate(
        "coherence",
        COHERENCE_RUBRIC,
        reference_examples if reference_examples is not None else REFERENCE_EXAMPLES,
        text,
    )


async def evaluate_vocabulary(
    text: str,
    reference_examples: list[ReferenceExample] | None = None,
) -> EvaluationResult:
    return await _evaluate(
        "vocabulary",
        VOCABULARY_RUBRIC,
        reference_examples if reference_examples is not None else REFERENCE_EXAMPLES,
        text,
    )


async def evaluate_readability(
    text: str,
    reference_examples: list[ReferenceExample] | None = None,
) -> EvaluationResult:
    return await _evaluate(
        "readability",
        READABILITY_RUBRIC,
        reference_examples if reference_examples is not None else REFERENCE_EXAMPLES,
        text,
    )


async def evaluate_task_fulfilment(
    text: str,
    reference_examples: list[ReferenceExample] | None = None,
) -> EvaluationResult:
    return await _evaluate(
        "task_fulfilment",
        TASK_FULFILMENT_RUBRIC,
        reference_examples if reference_examples is not None else REFERENCE_EXAMPLES,
        text,
    )
