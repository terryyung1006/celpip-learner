import inspect
import pytest


def test_run_agent_is_importable():
    from agent import run_agent
    assert callable(run_agent)


def test_run_agent_is_async():
    from agent import run_agent
    assert inspect.iscoroutinefunction(run_agent)


def test_main_is_importable():
    from agent import main
    assert callable(main)
