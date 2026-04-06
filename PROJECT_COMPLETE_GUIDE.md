# 911 Dispatch Project - Complete Beginner Guide

## 1. What this project is (in plain language)

This project is a simulator where an AI agent learns to behave like a city emergency dispatch supervisor.

Think of it like a strategy game:
- There are emergencies (incidents).
- There are responders (fire, police, EMS units).
- The agent must choose what to do each turn (dispatch, reassign, cancel, request mutual aid, etc.).
- The simulator gives a score for each decision and a final score for the whole run.

The goal is to train and evaluate decision-making quality under pressure.

## 2. What an RL environment means

RL means Reinforcement Learning.

In RL, four core ideas exist:
- Agent: the decision-maker (your model or baseline policy).
- Environment: the world that reacts to actions (this simulator).
- Reward: a number that says how good/bad the last action outcome was.
- Episode: one complete run from start to finish.

For this project:
- Agent picks an action.
- Environment updates city state.
- Environment returns:
  - updated observation,
  - reward,
  - done flag (whether run is over).

That loop repeats until the episode ends.

## 3. Important clarification: "scheme of electricity" vs "city schema"

There is no electricity scheme in this codebase.

What exists is a city schema.

City schema means a configuration blueprint for the simulation:
- city size (grid),
- districts,
- available units,
- unit speeds,
- default recommended unit types for each incident type.

The schema is loaded from data files and used to initialize deterministic, repeatable scenarios.

## 4. Project architecture (high level)

1. Scenario/task setup
- A task fixture builds initial units/incidents and metadata.

2. State machine update engine
- Validates actions.
- Applies action effects.
- Advances time by one tick.
- Updates incident statuses and unit statuses.

3. Reward + scoring
- Computes per-step reward components.
- Computes episode-level score using task-specific graders.

4. API server
- Exposes reset/step/state endpoints.

5. Dashboard
- Polls backend state repeatedly and renders units/incidents + reward bars.

## 5. What is the task?

A task is a scenario type with its own initial conditions, difficulty, and final grading logic.

This project has 4 tasks:

1. single_incident (easy)
- One incident, small unit pool.
- Focus: dispatch the right unit fast.

2. multi_incident (medium)
- Multiple incidents at the same time.
- Focus: triage/prioritization and handling P1 incidents.

3. mass_casualty (hard)
- Incident waves with severe emergencies and resource conflicts.
- Focus: survival outcomes under surge.

4. shift_surge (hard)
- New incidents arrive over time and some units go out of service.
- Focus: long-horizon operations and city coverage under degradation.

## 6. What is an episode?

An episode is one full run of a task from reset until terminal condition.

Episode starts when reset is called.
- step_count starts at 0.
- city_time starts at 0 seconds.
- units and incidents are loaded from selected task fixture.

Episode ends when any terminal condition is hit:
- max steps reached,
- at least one incident escalates,
- all incidents resolved.

## 7. What is a step?

A step is one action cycle:

1. Agent sends one action.
2. Validator checks if action is legal.
3. State machine applies action effects.
4. Time advances by 30 seconds.
5. Reward is computed.
6. Observation + reward + done are returned.

Important:
- step_count increases by 1 per step.
- city_time increases by 30 seconds per step.

## 8. At what step are we right now?

Snapshot from the live backend at the time this guide was generated:

- task_id: multi_incident
- episode_id: d2cd525e-2596-44cb-bbe3-af33236264a0
- step_count: 8
- city_time: 240.0 seconds
- cumulative_reward: 1.6
- episode_score: 0.0
- legal_actions currently available: 36

This is a live value, not a constant. If you reset again, step_count returns to 0.

## 9. Action space (what actions exist)

Current action types include:
- DISPATCH
- CANCEL
- REASSIGN
- STAGE
- MUTUAL_AID
- UPGRADE
- DOWNGRADE

Legal actions are generated from current state and filtered by protocol validation, so only valid actions appear in legal_actions.

## 10. How scoring works (complete detail)

There are two scoring layers:

1. Step reward (every action)
2. Episode score (whole run)

### 10.1 Step reward (RewardCalculator)

Step reward uses a weighted sum of 5 components:
- response_time: 30%
- triage: 25%
- survival: 25%
- coverage: 12%
- protocol: 8%

Total formula:
- total = 0.30 * response_time + 0.25 * triage + 0.25 * survival + 0.12 * coverage + 0.08 * protocol
- result is clamped to [0, 1]

Safety rule:
- If any Priority-1 incident existed and survival component is 0, total score is capped at 0.2.

Component details:

1. response_time
- Only meaningful for DISPATCH.
- For non-DISPATCH actions it returns neutral 0.5.
- For DISPATCH: compares ETA to severity benchmark.

2. triage
- Only meaningful for DISPATCH.
- Checks if dispatched unit type matches required unit types for incident type.
- Handles enum-qualified metadata keys safely.

3. survival
- Based on P1 incidents seen vs resolved without failure.
- Uses metadata lists: p1_seen, resolved_incidents, failed_incidents.

4. coverage
- Measures how many districts still have AVAILABLE coverage.

5. protocol
- If action invalid: 0.0.
- If valid and no phraseology text in Action.notes: neutral 0.5.
- If Action.notes provided: uses PhraseologyJudge score + readback correctness.

### 10.2 Episode score (whole run)

Episode score is task-specific via a central grade_episode router.

Why this matters:
- Different tasks need different definitions of success.
- Mean step reward alone is often too weak for real evaluation.

Task-specific episode graders:

1. single_incident
- +0.50 if incident resolved
- +0.30 if MEDIC dispatched correctly
- +0.20 if resolved within first 10 steps

2. multi_incident
- Uses P1 resolution, overall resolution ratio, and escalation penalty
- score = 0.5 * p1_score + 0.3 * resolution_score - 0.2 * failure_penalty

3. mass_casualty
- Emphasizes P1 survival with penalties for failures
- score = 0.6 * survival_score + 0.3 * mean_reward - failure_penalty

4. shift_surge (improved)
- Emphasizes long-horizon operational quality:
  - incident throughput (resolved ratio)
  - P1 survival
  - coverage
  - low backlog
  - mean reward
  - escalation penalty

## 11. Very important score semantics

In the OpenEnv wrapper:
- reward return value from step is per-step reward.
- observation.score is overwritten to episode score.

Also stored in metadata:
- cumulative_reward: running sum of step rewards.
- episode_rewards: list of per-step rewards.
- episode_score: current episode-level grade.

So if you compare values:
- reward = immediate local quality for this action
- observation.score = global task progress quality for the run

## 12. Is the dashboard connected to backend or just static?

It is connected to backend.

How we know:
- The dashboard JavaScript calls API endpoint http://localhost:8000/dashboard/state.
- It polls every 500 ms.
- It renders live units/incidents, step, and reward breakdown from backend response.

Connection behavior:
- If backend is unreachable, dashboard shows disconnected status.
- If backend is running and reset was called, dashboard updates live as step changes.

## 13. Why we used Docker

Docker is used to package the app and dependencies so it runs consistently everywhere.

Benefits:
- Same runtime on your machine, CI, and deployment platforms.
- No "works on my machine" package mismatch issues.
- Easy deployment with a single container image.
- Port compatibility: server reads PORT environment variable (important for hosted platforms).

In this project:
- Root Dockerfile runs uvicorn on 0.0.0.0 and PORT (default 8000).
- That makes it suitable for local run and hosted environments.

## 14. What API key are we using?

The project expects environment variables. Keys are not hardcoded in repository files.

Required for LLM mode:
- API_BASE_URL
- MODEL_NAME
- OPENAI_API_KEY

Compatibility fallback:
- HF_TOKEN is accepted if OPENAI_API_KEY is not set.

No-key mode:
- USE_RANDOM=true bypasses LLM and uses a deterministic random baseline agent.

Practical meaning:
- If USE_RANDOM=true, you can run without any API key.
- If USE_RANDOM is not true, OPENAI_API_KEY (or HF_TOKEN fallback) is needed.

## 15. Backend API endpoints (what each does)

- GET /health
  - health check

- GET /tasks
  - list available tasks

- POST /reset
  - start new episode for selected task

- POST /step
  - apply one action and move simulation one step

- GET /state
  - current state

- GET /dashboard/state
  - extended state for HTML dashboard (includes legal actions + last observation)

- GET /metadata and GET /schema
  - environment metadata and contracts

- POST /mcp
  - minimal JSON-RPC endpoint

## 16. What the dashboard shows vs what it does not show

Shows:
- Unit cards (status, assignment, ETA, location)
- Incident cards (type, severity, status, assigned units)
- Map view for units/incidents
- Last step reward component bars
- Header task/episode/step values

Nuance:
- Header "Score" currently uses metadata.cumulative_reward.
- Episode score is available too (metadata.episode_score), but not currently shown as the main header score.

## 17. Beginner glossary

- incident: emergency case to be handled
- unit: responder vehicle/team (EMS, fire, police, etc.)
- legal action: an action that passes protocol checks in current state
- reward: immediate feedback signal for one step
- episode score: overall quality of a full run
- terminal: episode is finished

## 18. Practical "how to think" summary

When you judge behavior quality in this project:
- Use step rewards to understand local tactical quality.
- Use episode score to understand mission success for the selected task.
- Use dashboard to observe live state transitions.
- Use task definitions to interpret what success means in each scenario.

If you remember one thing:
- This is not a generic chatbot app. It is a decision simulator where actions change a world state over time and are graded both step-by-step and across full episodes.
