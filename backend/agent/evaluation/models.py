from dataclasses import dataclass
from typing import Literal

Criterion = Literal["coherence", "vocabulary", "readability", "task_fulfilment"]
TaskType = Literal["task_1_email", "task_2_survey"]


@dataclass
class ReferenceExample:
    text: str
    band_score: int
    task_type: TaskType
    analysis: str = ""


@dataclass
class EvaluationResult:
    criterion: Criterion
    band_score: int
    feedback: str
