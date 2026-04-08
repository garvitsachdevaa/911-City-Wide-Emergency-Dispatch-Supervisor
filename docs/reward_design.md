# Reward Design — 911 Dispatch Supervisor

## Philosophy

The reward function is designed around one principle: **life before property, speed before coverage**. Every component weight reflects real dispatch priority doctrine.

## Components

| Component | Weight | What it measures |
|---|---|---|
| Response Time | 30% | How fast the correct unit reaches the incident |
| Triage | 25% | Whether unit type matches incident type (MEDIC→medical, ENGINE→fire) |
| Survival | 25% | Whether P1 patients survive to resolution |
| Coverage | 12% | Whether city districts have available units nearby |
| Protocol | 8% | Whether dispatch notes use realistic radio phraseology |

## Safety Gate

If **any** Priority-1 incident results in zero survival (patient died, or unit never arrived), the total episode reward is hard-capped at **0.2** — regardless of how well the agent performed on all other incidents.

This is not a bug. It reflects real dispatch accountability: no amount of good coverage or fast response on secondary incidents excuses a preventable P1 death.

## Partial Progress

Rewards are non-sparse. An agent receives signal every step for:
- Units moving toward incidents (ETA decreasing)
- Correct unit types being dispatched
- Districts maintaining coverage

This means even a weak agent that dispatches randomly receives informative gradient signal, making the environment suitable for both RL training and LLM evaluation.

## Difficulty Gradient

| Task | Random Score | LLM Expected | Design Intent |
|---|---|---|---|
| single_incident | 0.20 | 0.55–0.75 | One decision, one unit — tests basic triage |
| multi_incident | 0.31 | 0.40–0.60 | Competing P1s — tests priority ordering |
| mass_casualty | ~0.28 | 0.30–0.50 | Surprise waves — tests adaptability |
| shift_surge | ~0.25 | 0.25–0.40 | Resource scarcity — tests planning under constraint |

The gap between random and LLM scores is the signal this benchmark measures.
A model that scores 0.70 on single_incident but 0.25 on shift_surge is demonstrating
exactly the capability boundary the environment is designed to expose.
