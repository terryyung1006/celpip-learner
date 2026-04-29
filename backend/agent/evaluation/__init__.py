"""Public API for the CELPIP evaluation package."""
from agent.evaluation.models import EvaluationResult, ReferenceExample, Criterion, TaskType
from agent.evaluation.rubrics import (
    COHERENCE_RUBRIC,
    VOCABULARY_RUBRIC,
    READABILITY_RUBRIC,
    TASK_FULFILMENT_RUBRIC,
)
from agent.evaluation.reference_examples import REFERENCE_EXAMPLES
from agent.evaluation.skills import (
    evaluate_coherence,
    evaluate_vocabulary,
    evaluate_readability,
    evaluate_task_fulfilment,
)

__all__ = [
    "EvaluationResult",
    "ReferenceExample",
    "Criterion",
    "TaskType",
    "COHERENCE_RUBRIC",
    "VOCABULARY_RUBRIC",
    "READABILITY_RUBRIC",
    "TASK_FULFILMENT_RUBRIC",
    "REFERENCE_EXAMPLES",
    "evaluate_coherence",
    "evaluate_vocabulary",
    "evaluate_readability",
    "evaluate_task_fulfilment",
]
