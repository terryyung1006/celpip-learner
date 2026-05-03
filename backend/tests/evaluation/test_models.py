import pytest
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


def test_reference_example_rejects_out_of_range_band_score():
    with pytest.raises(ValueError, match="band_score must be 1"):
        ReferenceExample(text="x", band_score=13, task_type="task_1_email")


def test_evaluation_result_rejects_out_of_range_band_score():
    with pytest.raises(ValueError, match="band_score must be 1"):
        EvaluationResult(criterion="coherence", band_score=0, feedback="ok")


def test_package_exports_all_public_symbols():
    import agent.evaluation as pkg
    for name in pkg.__all__:
        assert hasattr(pkg, name), f"{name!r} in __all__ but not importable"
