# Architecture — 911 Dispatch Supervisor

## Layer Overview
OpenEnvEnvironment          ← public API (reset/step/state/legal_actions)
│
DispatchStateMachine        ← simulation engine
├── DispatchProtocolValidator   ← action legality (15+ rules)
├── RewardCalculator            ← 5-component weighted reward
└── DispatchScenarioFactory     ← deterministic task fixtures
│
Task-Specific Graders          ← episode-level scoring

## Key Design Decisions

### Why Manhattan Distance Physics
Real city blocks use Manhattan (rectilinear) distance for navigation.
Euclidean distance would underestimate travel time by ~27% on average,
making ETAs unrealistically optimistic. Manhattan physics produce ETAs
that match real CAD system calculations.

### Why Legal Actions Are Pre-filtered
Rather than letting agents propose arbitrary actions and penalizing illegal
ones, the environment exposes only currently-valid actions via `legal_actions()`.
This eliminates wasted LLM budget on invalid action generation and focuses
evaluation on dispatch decision quality, not action syntax compliance.

### Why the Safety Gate Uses 0.2 Not 0.0
A hard zero for any P1 failure would make the reward surface completely flat
for bad agents — no gradient to learn from. Capping at 0.2 preserves partial
signal (coverage, response time on other incidents) while making P1 failure
unambiguously catastrophic. Real dispatch accountability works the same way:
an incident review happens, but other good work is still acknowledged.

### Why Phraseology Is Scored
Real dispatchers are evaluated on radio communication clarity. An agent that
dispatches the right unit but says nothing (or says the wrong thing) is less
useful as a CAD copilot than one that also generates the correct radio traffic.
Phraseology scoring creates incentive for agents to learn domain language, not
just resource allocation.

### Why Waves Spawn at Fixed Steps Not Random Times
Reproducibility is a first-class requirement. Fixed step offsets guarantee
identical episode structure across all runs, making score comparisons valid.
The challenge comes from the agent not knowing wave timing in advance — it
must react, not plan.

## State Machine Transitions
Unit:     AVAILABLE → DISPATCHED → ON_SCENE → AVAILABLE
↘️ STAGED     ↗️
Incident: PENDING → RESPONDING → ON_SCENE → RESOLVED
↘️ ESCALATED (survival clock expired)

## File Map

| File | Responsibility |
|---|---|
| `src/models.py` | All Pydantic data contracts |
| `src/state_machine.py` | Core simulation engine |
| `src/protocol.py` | Action legality validation |
| `src/rewards.py` | Reward calculation |
| `src/physics.py` | Manhattan distance, ETA, coverage |
| `src/phraseology.py` | Radio language scoring |
| `src/city_schema.py` | City topology loader |
| `src/tasks/registry.py` | Task definitions and fixtures |
| `src/openenv_environment.py` | OpenEnv API wrapper |
| `server/app.py` | FastAPI server |
