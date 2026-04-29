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
