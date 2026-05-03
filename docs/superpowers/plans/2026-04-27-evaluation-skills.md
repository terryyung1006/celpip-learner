# CELPIP Evaluation Skills — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement 4 CELPIP evaluation skills (Coherence, Vocabulary, Readability, Task Fulfilment) as async Python functions that call the LLM with embedded rubric text and calibration examples to return a band score (1–12) and written feedback.

**Architecture:** A new `backend/agent/evaluation/` package contains `models.py` (data structures), `rubrics.py` (rubric text constants from official CELPIP descriptors), `reference_examples.py` (Level 9 sample responses as calibration data), and `skills.py` (LLM-calling functions). The LLM is called via `claude_agent_sdk.query` and must respond with JSON `{"band_score": N, "feedback": "..."}`. Tests mock `query` to avoid real LLM calls. No DB — rubrics and examples are embedded constants; DB integration is a future task.

**Tech Stack:** Python 3.12, claude-agent-sdk, pytest, pytest-asyncio

---

## File Map

| File | Purpose |
|------|---------|
| `backend/agent/evaluation/__init__.py` | Package exports |
| `backend/agent/evaluation/models.py` | `EvaluationResult`, `ReferenceExample` dataclasses |
| `backend/agent/evaluation/rubrics.py` | Rubric text constants for all 4 criteria |
| `backend/agent/evaluation/reference_examples.py` | Level 9 sample responses (calibration data) |
| `backend/agent/evaluation/skills.py` | `_build_prompt`, `_evaluate`, + 4 public skill functions |
| `backend/tests/evaluation/__init__.py` | Empty package marker |
| `backend/tests/evaluation/test_models.py` | Dataclass structure tests |
| `backend/tests/evaluation/test_rubrics.py` | Rubric content and reference example tests |
| `backend/tests/evaluation/test_skills.py` | LLM-mocked skill tests |

---

## Task 1: Data models

**Files:**
- Create: `backend/agent/evaluation/__init__.py`
- Create: `backend/agent/evaluation/models.py`
- Create: `backend/tests/evaluation/__init__.py`
- Create: `backend/tests/evaluation/test_models.py`

- [ ] **Step 1: Create empty package markers**

Create `backend/agent/evaluation/__init__.py` (empty file — will be populated in Task 4).

Create `backend/tests/evaluation/__init__.py` (empty file).

- [ ] **Step 2: Write the failing test — create `backend/tests/evaluation/test_models.py`**

```python
from agent.evaluation.models import EvaluationResult, ReferenceExample


def test_evaluation_result_stores_fields():
    result = EvaluationResult(criterion="coherence", band_score=9, feedback="Strong coherence.")
    assert result.criterion == "coherence"
    assert result.band_score == 9
    assert result.feedback == "Strong coherence."


def test_reference_example_defaults_empty_analysis():
    ex = ReferenceExample(text="Sample text.", band_score=9, task_type="task_1_email")
    assert ex.text == "Sample text."
    assert ex.band_score == 9
    assert ex.task_type == "task_1_email"
    assert ex.analysis == ""


def test_reference_example_stores_analysis():
    ex = ReferenceExample(
        text="Text.", band_score=9, task_type="task_2_survey", analysis="Good vocab."
    )
    assert ex.analysis == "Good vocab."
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd backend && uv run pytest tests/evaluation/test_models.py -v
```

Expected: `ImportError` — `agent.evaluation.models` not found.

- [ ] **Step 4: Create `backend/agent/evaluation/models.py`**

```python
from dataclasses import dataclass, field
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
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd backend && uv run pytest tests/evaluation/test_models.py -v
```

Expected:
```
PASSED tests/evaluation/test_models.py::test_evaluation_result_stores_fields
PASSED tests/evaluation/test_models.py::test_reference_example_defaults_empty_analysis
PASSED tests/evaluation/test_models.py::test_reference_example_stores_analysis
3 passed
```

- [ ] **Step 6: Commit**

```bash
git add backend/agent/evaluation/__init__.py backend/agent/evaluation/models.py backend/tests/evaluation/__init__.py backend/tests/evaluation/test_models.py
git commit -m "feat: add evaluation models (EvaluationResult, ReferenceExample)"
```

---

## Task 2: Rubrics and reference examples

**Files:**
- Create: `backend/agent/evaluation/rubrics.py`
- Create: `backend/agent/evaluation/reference_examples.py`
- Create: `backend/tests/evaluation/test_rubrics.py`

- [ ] **Step 1: Write the failing test — create `backend/tests/evaluation/test_rubrics.py`**

```python
from agent.evaluation.rubrics import (
    COHERENCE_RUBRIC,
    VOCABULARY_RUBRIC,
    READABILITY_RUBRIC,
    TASK_FULFILMENT_RUBRIC,
)
from agent.evaluation.reference_examples import REFERENCE_EXAMPLES


def test_all_rubrics_are_non_empty_strings():
    for rubric in [COHERENCE_RUBRIC, VOCABULARY_RUBRIC, READABILITY_RUBRIC, TASK_FULFILMENT_RUBRIC]:
        assert isinstance(rubric, str)
        assert len(rubric) > 50


def test_all_rubrics_mention_band_9():
    for rubric in [COHERENCE_RUBRIC, VOCABULARY_RUBRIC, READABILITY_RUBRIC, TASK_FULFILMENT_RUBRIC]:
        assert "Band 9" in rubric


def test_all_rubrics_mention_band_8():
    for rubric in [COHERENCE_RUBRIC, VOCABULARY_RUBRIC, READABILITY_RUBRIC, TASK_FULFILMENT_RUBRIC]:
        assert "Band 8" in rubric


def test_reference_examples_has_four_entries():
    assert len(REFERENCE_EXAMPLES) == 4


def test_reference_examples_include_band_9_and_band_8():
    band_scores = {ex.band_score for ex in REFERENCE_EXAMPLES}
    assert 9 in band_scores
    assert 8 in band_scores


def test_reference_examples_cover_both_task_types():
    task_types = {ex.task_type for ex in REFERENCE_EXAMPLES}
    assert "task_1_email" in task_types
    assert "task_2_survey" in task_types
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && uv run pytest tests/evaluation/test_rubrics.py -v
```

Expected: `ImportError` — modules not found.

- [ ] **Step 3: Create `backend/agent/evaluation/rubrics.py`**

```python
COHERENCE_RUBRIC = """CELPIP Writing — Content/Coherence Criterion

Band 9 indicators:
- Write short formal and informal texts of some complexity. Complexity is more consistent
  than at lower bands.
- Support key ideas with relevant facts, descriptions, details, or quotations. Ideas are
  supported with both relevant personal details and facts/descriptions (e.g., information
  about school and work schedules; explanation of the results of cutting back a service).

Band 8 indicators:
- Write short, moderately complex texts. More complexity in ideas than at Band 7 but less
  consistently developed than Band 9.
- Develop a main idea with supporting details. Supporting details are more specific and less
  repetitive than at Band 7 (e.g., specific personal scenarios and community-level reasoning).

Scoring guidance:
- Band 10–12: Complexity is very consistent; key ideas are thoroughly and precisely supported
  with multiple types of evidence.
- Band 7: Texts show some complexity; key ideas are supported but development is uneven or
  repetitive.
- Band 5–6: Texts are mostly simple in structure; key ideas may be stated without adequate
  support or development.
- Band 1–4: Texts are very short or simple; key ideas are absent or unsupported.
"""

VOCABULARY_RUBRIC = """CELPIP Writing — Vocabulary Criterion

Band 9 indicators:
- Choose words and phrases to provide accurate details, descriptions, and comparisons.
  Vocabulary facilitates communication of accurate details about both personal matters and
  broader issues.
- Few errors in vocabulary. Words that effectively indicate comparison are used
  (e.g., "as opposed to", "more efficient").

Band 8 indicators:
- Use common or context-specific words to communicate meaning. Meaning is communicated more
  precisely and concisely than at Band 7.
- Common words and phrases used appropriately (e.g., "work late", "hang out", "about right").
- Some context-specific words and expressions used (e.g., "a regular patron", "family friendly",
  "junk mails", "preferred mode of correspondence").

Scoring guidance:
- Band 10–12: Word choices are precise and varied throughout; virtually no errors.
- Band 7: Vocabulary is generally adequate; meaning is communicated but with less precision
  and conciseness than Band 8.
- Band 5–6: Vocabulary is limited or repetitive; some errors that occasionally impede meaning.
- Band 1–4: Very limited vocabulary; frequent errors that impede comprehension.
"""

READABILITY_RUBRIC = """CELPIP Writing — Readability Criterion

Band 9 indicators:
- Write well-organized paragraphs. Each paragraph contains one clear main idea developed
  with supporting details in an easy-to-read way.
- Write with control of a range of complex and diverse grammatical structures. Control is
  noticeably strong; errors are infrequent and have minimal impact on readability.
- Create complex sentences using conditionals/hypotheticals (e.g., "it would be much easier
  if") and a wide variety of transitions and conjunctions (e.g., "as a result", "in turn",
  "instead of", "as opposed to").
- Write with good control of spelling and punctuation. Spelling errors are rare; punctuation
  is mostly correct.

Band 8 indicators:
- Write well-organized paragraphs with a clear main idea per paragraph.
- Write with good control of complex grammatical structures, spelling, and punctuation.
  Quite a few errors are present but they generally don't impede comprehension of ideas.

Scoring guidance:
- Band 10–12: Paragraphs are tightly organised; grammar is highly accurate; complex structures
  used with ease; virtually no spelling or punctuation errors.
- Band 7: Paragraphs are generally organised; grammar is mostly accurate with more errors than
  Band 8; complex structures attempted with partial success.
- Band 5–6: Paragraph organisation is inconsistent; grammar errors are noticeable but
  communication is maintained; spelling and punctuation errors are frequent.
- Band 1–4: Little or no paragraph structure; frequent grammar, spelling, and punctuation
  errors that impede understanding.
"""

TASK_FULFILMENT_RUBRIC = """CELPIP Writing — Task Fulfilment Criterion

Band 9 indicators:
- Present information using a tone and style that follows some formal and most informal
  writing conventions. The tone of the response is consistently appropriate. Standard
  phrases and devices for formal correspondence are used (e.g., "I am writing to you today
  regarding…", polite modal verbs, clear opening and closing statements).
- Convey the intended meaning. The writer successfully conveys everything intended to be
  communicated.

Band 8 indicators:
- Present information using a tone and style that follows common writing conventions.
  Responses contain an appropriate mix of relevant personal information and ideas with a
  wider/less personal scope (e.g., community benefits, institutional trends).
- Convey and support main ideas about a topic. Contextually appropriate style is used
  (e.g., "I am writing to you with regards to", "I would appreciate", "I will look forward
  to your favourable response").

Scoring guidance:
- Band 10–12: Tone and style fully meet all formal and informal conventions; meaning is
  conveyed completely and precisely.
- Band 7: Tone and style are mostly appropriate with minor lapses; intended meaning is
  conveyed though some details may be missing or unclear.
- Band 5–6: Tone and style are somewhat appropriate; the response addresses the task but
  some parts are incomplete or off-topic.
- Band 1–4: Tone and style are largely inappropriate; the response fails to address key
  parts of the task or meaning is unclear.
"""
```

- [ ] **Step 4: Create `backend/agent/evaluation/reference_examples.py`**

```python
from agent.evaluation.models import ReferenceExample

TASK_A_LEVEL_9 = ReferenceExample(
    text=(
        "To whom it may concern,\n\n"
        "My name is Seth and I am writing to you today regarding the opening hours for the library. "
        "I am an English student and my course requires me to read many books throughout the year. "
        "As a result, I visit the library several times a week to rent the required books. "
        "Books can be very expensive, so the library is a great benefit to me as instead of spending "
        "lots of money buying these expensive books I can rent them instead at a much lower cost.\n\n"
        "I have recently started a new part-time job. Now, my only days off are Sundays and Tuesdays. "
        "The library is closed on Sundays which leaves Tuesday evenings after school as the only time "
        "I can visit the library. As the library closes early on Tuesdays, I have to rush down after "
        "school. This is very stressful for me and it would be much easier if the Library was open on "
        "Sundays as then I would have all day to visit.\n\n"
        "I feel that many other people have the same problem and would benefit greatly if the library "
        "was open every day. I hope you will consider this.\n\n"
        "Thanks,\nSeth"
    ),
    band_score=9,
    task_type="task_1_email",
    analysis=(
        "Content/Coherence: Both tasks are complex with consistent development. Ideas are supported "
        "with personal details (school/work schedule) and broader facts.\n"
        "Vocabulary: Word choices provide accurate details; few errors (most notable: 'rent' instead "
        "of 'borrow'). Comparison words used effectively.\n"
        "Readability: Each paragraph has one clear main idea with supporting details. Grammar control "
        "is strong; errors are infrequent. Complex structures include conditionals ('it would be much "
        "easier if') and varied conjunctions ('as a result', 'instead of').\n"
        "Task Fulfilment: Tone is consistently appropriate. Standard formal phrases used "
        "('I am writing to you today regarding'). Intended meaning is conveyed (though third "
        "sub-task is not fully addressed)."
    ),
)

TASK_B_LEVEL_9 = ReferenceExample(
    text=(
        "I would prefer to have my mail delivered to my home twice a week as opposed to me collecting "
        "it myself at the local post office. The reason I would prefer this is because I have a very "
        "busy schedule and having to collect my own mail from the post office would just take up more "
        "of my spare time. Also, the closest post office to my house is a twenty minute walk. I do not "
        "own a car so I would have to walk this distance in order to collect my mail.\n\n"
        "I feel that having my mail delivered to my home twice a week is a more efficient way of "
        "delivering mail to homes as it limits the amounts of trips the post office has to take in "
        "order to deliver mail. This in turn will save money for the government as instead of spending "
        "money on gas and wages for the employees that deliver the mail every day, they will be only "
        "spending this money two days per week.\n\n"
        "These are the reason I would prefer to have my mail sent out to my home twice a week."
    ),
    band_score=9,
    task_type="task_2_survey",
    analysis=(
        "Content/Coherence: Text is complex with consistent development. Ideas are supported with "
        "personal details (schedule, distance to post office) and broader facts (cost savings).\n"
        "Vocabulary: Accurate and varied; comparison words used effectively "
        "('as opposed to', 'more efficient').\n"
        "Readability: Well-organised paragraphs, each with a clear main idea. Strong grammatical "
        "control; complex structures used ('in turn', 'instead of', 'as opposed to').\n"
        "Task Fulfilment: Tone is consistently appropriate for a survey response. Intended meaning "
        "is fully conveyed."
    ),
)

TASK_A_LEVEL_8 = ReferenceExample(
    text=(
        "Dear Chief Librarian,\n\n"
        "I am writing to you with regards to the operating hours of your library. I would appreciate "
        "that the library committee will consider operating on Sundays and Mondays as well.\n\n"
        "I am a regular patron of your library. I need to visit the library for my research and self "
        "study sessions required for my part time MBA course. Occasionally, I would be required to "
        "work late for meetings and overtime, and would not be meet the library operating hours. I "
        "could only use the library on Saturday, which is a day I would need to complete other "
        "household chores.\n\n"
        "By opening your library daily, it can benefit not just me, but the entire community. Most "
        "families will spend their Sundays doing things together. The library can certainly organize "
        "story telling sessions or talks/workshops that are family friendly on Sundays. There are also "
        "many schools surrounding your library. Your library is an excellent place for highschoolers "
        "to hang out after school for self studies or project meetings. Therefore, there is every "
        "reason to open on Mondays too!\n\n"
        "I hope my suggestions can be considered by the committee. I will look forward to your "
        "favourable response soon.\n\n"
        "Regards\n\nWendy"
    ),
    band_score=8,
    task_type="task_1_email",
    analysis=(
        "Content/Coherence: Main idea developed with supporting details; more specific and less "
        "repetitive than Band 7. Includes personal scenario (MBA course, work schedule) and "
        "community-level reasoning (family sessions, high school students).\n"
        "Vocabulary: Common words used appropriately ('work late', 'hang out', 'every reason', "
        "'community'). Context-specific phrases used ('a regular patron', 'family friendly').\n"
        "Readability: Well-organised paragraphs. Quite a few errors ('would not be meet', "
        "'story telling') but they generally don't impede comprehension.\n"
        "Task Fulfilment: Appropriate mix of personal information and wider community scope. "
        "Contextually appropriate formal phrases used ('I am writing to you with regards to', "
        "'I will look forward to your favourable response')."
    ),
)

TASK_B_LEVEL_8 = ReferenceExample(
    text=(
        "My option is to have my mails delivered to my home twice a week. Though it's only twice a "
        "week, but it does not change my daily routine. We do not need to allocate time for post "
        "office pick up. Sometimes, both my husband and myself may be too occupied at work, and may "
        "miss picking up the mails. I sincerely do not want to miss out important mails for that "
        "reason.\n\n"
        "Base on our mailing records, we do not receive mails daily. At least for relevant mails. "
        "We do have junk mails delivered daily, which is not favoured. We had opted for electronic "
        "mails for most of our banking and financial institutions. So we will not be expecting "
        "regular mails from them. Government bodies are also starting to mail electronically, which "
        "is the our preferred mode of correspondence. Twice a week of mail delivery is about right "
        "for our family. In fact, we do not require to clear our mailbox stuffed with junk mails "
        "everyday anymore!"
    ),
    band_score=8,
    task_type="task_2_survey",
    analysis=(
        "Content/Coherence: Main idea developed with supporting details; more specific than Band 7. "
        "Ideas include personal details (routine, husband's schedule) and broader institutional "
        "trends (banks and government shifting to electronic mail).\n"
        "Vocabulary: Common phrases used appropriately ('at work', 'about right', 'miss out'). "
        "Context-specific expressions used ('junk mails', 'preferred mode of correspondence').\n"
        "Readability: Paragraphs are well-organised. Quite a few errors ('Base on', 'the our') "
        "but they generally don't impede comprehension.\n"
        "Task Fulfilment: Appropriate mix of personal information and wider scope. Contextually "
        "appropriate style ('both my husband and myself may be too occupied')."
    ),
)

REFERENCE_EXAMPLES: list[ReferenceExample] = [
    TASK_A_LEVEL_9,
    TASK_B_LEVEL_9,
    TASK_A_LEVEL_8,
    TASK_B_LEVEL_8,
]
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd backend && uv run pytest tests/evaluation/test_rubrics.py -v
```

Expected:
```
PASSED tests/evaluation/test_rubrics.py::test_all_rubrics_are_non_empty_strings
PASSED tests/evaluation/test_rubrics.py::test_all_rubrics_mention_band_9
PASSED tests/evaluation/test_rubrics.py::test_all_rubrics_mention_band_8
PASSED tests/evaluation/test_rubrics.py::test_reference_examples_has_four_entries
PASSED tests/evaluation/test_rubrics.py::test_reference_examples_include_band_9_and_band_8
PASSED tests/evaluation/test_rubrics.py::test_reference_examples_cover_both_task_types
6 passed
```

- [ ] **Step 6: Commit**

```bash
git add backend/agent/evaluation/rubrics.py backend/agent/evaluation/reference_examples.py backend/tests/evaluation/test_rubrics.py
git commit -m "feat: add CELPIP rubric constants and Level 9 reference examples"
```

---

## Task 3: Evaluation skills

**Files:**
- Create: `backend/agent/evaluation/skills.py`
- Create: `backend/tests/evaluation/test_skills.py`

- [ ] **Step 1: Write the failing tests — create `backend/tests/evaluation/test_skills.py`**

```python
import pytest
from agent.evaluation.models import EvaluationResult, ReferenceExample


async def _mock_query(prompt):
    yield '{"band_score": 9, "feedback": "Strong coherence throughout the response."}'


@pytest.fixture
def mock_lm(monkeypatch):
    monkeypatch.setattr("agent.evaluation.skills.query", _mock_query)


# --- _build_prompt ---

def test_build_prompt_contains_rubric_and_user_text():
    from agent.evaluation.skills import _build_prompt
    from agent.evaluation.rubrics import COHERENCE_RUBRIC
    prompt = _build_prompt(
        "coherence",
        COHERENCE_RUBRIC,
        [ReferenceExample(text="Reference text.", band_score=9, task_type="task_1_email")],
        "User's writing sample.",
    )
    assert "Band 9" in prompt
    assert "Reference text." in prompt
    assert "User's writing sample." in prompt


def test_build_prompt_contains_criterion_label():
    from agent.evaluation.skills import _build_prompt
    prompt = _build_prompt(
        "task_fulfilment",
        "rubric text here",
        [ReferenceExample(text="Ref.", band_score=9, task_type="task_1_email")],
        "Text.",
    )
    assert "Task Fulfilment" in prompt


# --- evaluate_coherence ---

@pytest.mark.asyncio
async def test_evaluate_coherence_returns_result(mock_lm):
    from agent.evaluation.skills import evaluate_coherence
    result = await evaluate_coherence("Some article text about libraries.")
    assert isinstance(result, EvaluationResult)
    assert result.criterion == "coherence"
    assert result.band_score == 9
    assert len(result.feedback) > 0


# --- evaluate_vocabulary ---

@pytest.mark.asyncio
async def test_evaluate_vocabulary_returns_result(mock_lm):
    from agent.evaluation.skills import evaluate_vocabulary
    result = await evaluate_vocabulary("Some text.")
    assert result.criterion == "vocabulary"
    assert 1 <= result.band_score <= 12


# --- evaluate_readability ---

@pytest.mark.asyncio
async def test_evaluate_readability_returns_result(mock_lm):
    from agent.evaluation.skills import evaluate_readability
    result = await evaluate_readability("Some text.")
    assert result.criterion == "readability"
    assert 1 <= result.band_score <= 12


# --- evaluate_task_fulfilment ---

@pytest.mark.asyncio
async def test_evaluate_task_fulfilment_returns_result(mock_lm):
    from agent.evaluation.skills import evaluate_task_fulfilment
    result = await evaluate_task_fulfilment("Some text.")
    assert result.criterion == "task_fulfilment"
    assert 1 <= result.band_score <= 12


# --- custom reference examples ---

@pytest.mark.asyncio
async def test_evaluate_accepts_custom_reference_examples(mock_lm):
    from agent.evaluation.skills import evaluate_coherence
    custom = [ReferenceExample(text="Custom ref.", band_score=7, task_type="task_1_email")]
    result = await evaluate_coherence("Text.", reference_examples=custom)
    assert result.criterion == "coherence"


# --- error handling ---

@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_invalid_json(monkeypatch):
    async def bad_query(prompt):
        yield "not json at all"
    monkeypatch.setattr("agent.evaluation.skills.query", bad_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="invalid JSON"):
        await evaluate_coherence("Text.")


@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_out_of_range_band(monkeypatch):
    async def bad_band_query(prompt):
        yield '{"band_score": 13, "feedback": "out of range"}'
    monkeypatch.setattr("agent.evaluation.skills.query", bad_band_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="out of range"):
        await evaluate_coherence("Text.")
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd backend && uv run pytest tests/evaluation/test_skills.py -v
```

Expected: `ImportError` — `agent.evaluation.skills` not found.

- [ ] **Step 3: Create `backend/agent/evaluation/skills.py`**

```python
import json
from claude_agent_sdk import query
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
        parts.append(str(message))
    raw = "".join(parts)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {raw!r}") from e
    band_score = int(data["band_score"])
    if not 1 <= band_score <= 12:
        raise ValueError(f"band_score {band_score} out of range 1-12")
    return EvaluationResult(criterion=criterion, band_score=band_score, feedback=data["feedback"])


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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd backend && uv run pytest tests/evaluation/test_skills.py -v
```

Expected:
```
PASSED tests/evaluation/test_skills.py::test_build_prompt_contains_rubric_and_user_text
PASSED tests/evaluation/test_skills.py::test_build_prompt_contains_criterion_label
PASSED tests/evaluation/test_skills.py::test_evaluate_coherence_returns_result
PASSED tests/evaluation/test_skills.py::test_evaluate_vocabulary_returns_result
PASSED tests/evaluation/test_skills.py::test_evaluate_readability_returns_result
PASSED tests/evaluation/test_skills.py::test_evaluate_task_fulfilment_returns_result
PASSED tests/evaluation/test_skills.py::test_evaluate_accepts_custom_reference_examples
PASSED tests/evaluation/test_skills.py::test_evaluate_raises_value_error_on_invalid_json
PASSED tests/evaluation/test_skills.py::test_evaluate_raises_value_error_on_out_of_range_band
9 passed
```

- [ ] **Step 5: Commit**

```bash
git add backend/agent/evaluation/skills.py backend/tests/evaluation/test_skills.py
git commit -m "feat: add evaluation skills for all 4 CELPIP criteria"
```

---

## Task 4: Package exports

**Files:**
- Modify: `backend/agent/evaluation/__init__.py`
- Modify: `backend/tests/evaluation/test_models.py`

- [ ] **Step 1: Add export test to `backend/tests/evaluation/test_models.py`**

Append to the existing file:

```python
def test_package_exports_all_public_symbols():
    import inspect
    from agent import evaluation
    from agent.evaluation import (
        EvaluationResult,
        ReferenceExample,
        evaluate_coherence,
        evaluate_vocabulary,
        evaluate_readability,
        evaluate_task_fulfilment,
    )
    assert inspect.iscoroutinefunction(evaluate_coherence)
    assert inspect.iscoroutinefunction(evaluate_vocabulary)
    assert inspect.iscoroutinefunction(evaluate_readability)
    assert inspect.iscoroutinefunction(evaluate_task_fulfilment)
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd backend && uv run pytest tests/evaluation/test_models.py::test_package_exports_all_public_symbols -v
```

Expected: `ImportError` — cannot import from `agent.evaluation`.

- [ ] **Step 3: Update `backend/agent/evaluation/__init__.py`**

```python
from agent.evaluation.models import EvaluationResult, ReferenceExample
from agent.evaluation.skills import (
    evaluate_coherence,
    evaluate_vocabulary,
    evaluate_readability,
    evaluate_task_fulfilment,
)

__all__ = [
    "EvaluationResult",
    "ReferenceExample",
    "evaluate_coherence",
    "evaluate_vocabulary",
    "evaluate_readability",
    "evaluate_task_fulfilment",
]
```

- [ ] **Step 4: Run all evaluation tests**

```bash
cd backend && uv run pytest tests/evaluation/ -v
```

Expected: All 19 tests pass.

- [ ] **Step 5: Run full test suite to confirm no regressions**

```bash
cd backend && uv run pytest -v
```

Expected: All tests pass, including the original 3 smoke tests in `tests/test_agent.py`.

- [ ] **Step 6: Commit**

```bash
git add backend/agent/evaluation/__init__.py backend/tests/evaluation/test_models.py
git commit -m "feat: export evaluation package public API"
```

---

## Done

At this point the repo has:
- `backend/agent/evaluation/` — a complete, tested evaluation package
- 4 async skill functions: `evaluate_coherence`, `evaluate_vocabulary`, `evaluate_readability`, `evaluate_task_fulfilment`
- Rubric text for all 4 CELPIP criteria (Band 9 anchored with band-by-band guidance)
- Level 9 calibration reference examples embedded (both task types)
- 17 passing tests; no real LLM calls required
