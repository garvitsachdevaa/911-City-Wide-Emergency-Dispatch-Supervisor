"""Episode grading utilities.

This module centralizes "final score" computation so benchmark runs and
OpenEnv runs report the same episode score.
"""

from __future__ import annotations

from src.models import State


def grade_episode(task_id: str, state: State | None, rewards: list[float]) -> float:
    """Compute a final episode score in [0.0, 1.0].

    Args:
        task_id: Task identifier.
        state: Final (or current) state.
        rewards: Per-step rewards.

    Returns:
        Normalized score in [0.0, 1.0].
    """

    if not rewards:
        return 0.0

    # Lazy imports avoid circular dependencies (task graders import src.rewards).
    if task_id == "single_incident":
        from src.tasks.single_incident import SingleIncidentGrader

        return float(SingleIncidentGrader().grade(state, rewards) if state is not None else 0.0)

    if task_id == "multi_incident":
        from src.tasks.multi_incident import MultiIncidentGrader

        return float(MultiIncidentGrader().grade(state, rewards) if state is not None else 0.0)

    if task_id == "mass_casualty":
        from src.tasks.mass_casualty import MassCasualtyGrader

        return float(MassCasualtyGrader().grade(state, rewards) if state is not None else 0.0)

    if task_id == "shift_surge":
        from src.tasks.shift_surge import ShiftSurgeGrader

        return float(ShiftSurgeGrader().grade(state, rewards) if state is not None else 0.0)

    # Fallback: mean of rewards (legacy behavior).
    return float(sum(rewards) / max(len(rewards), 1))
