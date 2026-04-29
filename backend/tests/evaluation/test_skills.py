import pytest
from claude_agent_sdk.types import AssistantMessage, TextBlock
from agent.evaluation.models import EvaluationResult, ReferenceExample


def _make_assistant_message(text: str) -> AssistantMessage:
    return AssistantMessage(content=[TextBlock(text=text)], model="claude-test")


async def _mock_query(prompt):
    yield _make_assistant_message('{"band_score": 9, "feedback": "Strong coherence throughout the response."}')


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
async def test_evaluate_uses_custom_reference_examples(monkeypatch):
    captured = {}

    async def capturing_query(prompt):
        captured["prompt"] = prompt
        yield _make_assistant_message('{"band_score": 9, "feedback": "test"}')

    monkeypatch.setattr("agent.evaluation.skills.query", capturing_query)
    from agent.evaluation.skills import evaluate_coherence
    custom = [ReferenceExample(text="Custom ref.", band_score=7, task_type="task_1_email")]
    result = await evaluate_coherence("Text.", reference_examples=custom)
    assert result.criterion == "coherence"
    assert "Custom ref." in captured["prompt"]


# --- error handling ---

@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_empty_response(monkeypatch):
    async def empty_query(prompt):
        return
        yield  # make it an async generator
    monkeypatch.setattr("agent.evaluation.skills.query", empty_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="empty response"):
        await evaluate_coherence("Text.")


@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_invalid_json(monkeypatch):
    async def bad_query(prompt):
        yield _make_assistant_message("not json at all")
    monkeypatch.setattr("agent.evaluation.skills.query", bad_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="invalid JSON"):
        await evaluate_coherence("Text.")


@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_out_of_range_band(monkeypatch):
    async def bad_band_query(prompt):
        yield _make_assistant_message('{"band_score": 13, "feedback": "out of range"}')
    monkeypatch.setattr("agent.evaluation.skills.query", bad_band_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="out of range"):
        await evaluate_coherence("Text.")


@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_band_score_zero(monkeypatch):
    async def zero_band_query(prompt):
        yield _make_assistant_message('{"band_score": 0, "feedback": "out of range"}')
    monkeypatch.setattr("agent.evaluation.skills.query", zero_band_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="out of range"):
        await evaluate_coherence("Text.")


@pytest.mark.asyncio
async def test_evaluate_raises_value_error_on_bool_band_score(monkeypatch):
    async def bool_band_query(prompt):
        yield _make_assistant_message('{"band_score": true, "feedback": "bool"}')
    monkeypatch.setattr("agent.evaluation.skills.query", bool_band_query)
    from agent.evaluation.skills import evaluate_coherence
    with pytest.raises(ValueError, match="must be an integer"):
        await evaluate_coherence("Text.")
