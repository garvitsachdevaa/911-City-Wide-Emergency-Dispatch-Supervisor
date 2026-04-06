"""Integration tests for benchmark assembly and score ranges."""

from __future__ import annotations

import asyncio

from src.models import Action, DispatchAction
from src.benchmark import list_tasks, run_all, run_task
from src.openenv_environment import OpenEnvEnvironment


def test_list_tasks_has_four() -> None:
    tasks = list_tasks()
    assert len(tasks) == 4
    ids = {t["task_id"] for t in tasks}
    assert ids == {"single_incident", "multi_incident", "mass_casualty", "shift_surge"}


def test_run_task_score_in_range() -> None:
    result = run_task("single_incident", seed=42)
    assert 0.0 <= result["score"] <= 1.0
    assert result["task_id"] == "single_incident"


def test_benchmark_and_openenv_use_same_episode_grader(monkeypatch) -> None:
    from src.tasks.single_incident import SingleIncidentGrader

    expected_score = 0.777
    monkeypatch.setattr(SingleIncidentGrader, "grade", lambda self, state, rewards: expected_score)

    # Benchmark path.
    result = run_task("single_incident", seed=42)
    assert abs(result["score"] - expected_score) < 1e-9

    # OpenEnv path.
    env = OpenEnvEnvironment(task_id="single_incident", seed=42)
    asyncio.run(env.reset())
    obs, reward, done = asyncio.run(
        env.step(
            Action(
                action_type=DispatchAction.DISPATCH,
                unit_id="MED-1",
                incident_id="INC-001",
            )
        )
    )
    assert isinstance(reward, float)
    assert isinstance(done, bool)
    assert abs(float(obs.score) - expected_score) < 1e-9
    env.close()


def test_run_all_scores_in_range() -> None:
    scores = run_all()
    assert set(scores.keys()) == {"single_incident", "multi_incident", "mass_casualty", "shift_surge"}
    assert all(0.0 <= s <= 1.0 for s in scores.values())
