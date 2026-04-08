import re

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# A3 replacements
readme = readme.replace(
    "**What a good agent does**: Immediately dispatches `MED-1 → INC-001`.",
    "**What a good agent does**: Immediately dispatches `MED-1 → INC-001`.\n\n**Scoring:** 50% resolution + 30% correct unit type used + 20% response speed."
)

readme = readme.replace(
    "**What a good agent does**: Immediately dispatches MEDIC to cardiac arrest and patrol to shooting, then handles the fire with ENGINE/LADDER.",
    "**What a good agent does**: Immediately dispatches MEDIC to cardiac arrest and patrol to shooting, then handles the fire with ENGINE/LADDER.\n\n**Scoring:** 50% P1 resolution + 30% overall resolution − 20% escalation penalty."
)

readme = readme.replace(
    "**What a good agent does**: Dispatches immediately to initial collapse, stages additional units near expected wave arrival zones, requests mutual aid for later waves.",
    "**What a good agent does**: Dispatches immediately to initial collapse, stages additional units near expected wave arrival zones, requests mutual aid for later waves.\n\n**Scoring:** 60% P1 survival + 30% mean step reward − failure penalty if building collapse unresponded."
)

readme = readme.replace(
    "**Why it's hard**: No single optimal strategy — agents must continuously rebalance between throughput and coverage as available resources shrink and incident demand grows.",
    "**Why it's hard**: No single optimal strategy — agents must continuously rebalance between throughput and coverage as available resources shrink and incident demand grows.\n\n**Scoring:** 35% resolution + 25% P1 survival + 15% coverage + 15% backlog management + 10% step reward − 25% escalation penalty."
)

# A4 replacements
a4_addition = """
### What the scores mean

A random agent scoring **0.20 on the easiest task** confirms the environment is not trivially solvable — there is no reward for random dispatching. The gradient from 0.20 → 0.46 across tasks reflects genuine increasing complexity, not just more steps.

A well-prompted frontier LLM (GPT-4o, Llama-3.1-70B) is expected to score **0.55–0.75 on single_incident** and **0.30–0.45 on shift_surge**, demonstrating the environment meaningfully differentiates agent capability.
"""

# We'll insert A4 right after the NOTE blockquote below the baseline score table.
# Existing note text: > **Note:** Earlier README versions showed higher scores (~0.30–0.74) from a different scoring path (`observation.score`). These figures use the canonical competition normalization: `sum(step_rewards) / max_steps`, clamped to `[0.0, 1.0]`.

readme = readme.replace(
    "clamped to `[0.0, 1.0]`.\n",
    f"clamped to `[0.0, 1.0]`.\n\n{a4_addition.strip()}\n"
)

# D1 replacements (Phraseology examples)
d1_addition = """
#### Dispatch Phraseology (bonus scoring)

The `notes` field is scored for realistic radio communication language. Agents that use proper dispatch phraseology receive up to 8% bonus on their protocol score.

| Action | Example notes value |
|---|---|
| Dispatch MEDIC to cardiac | `"Medic 1 en route to cardiac arrest, Code 3, ETA 4 minutes"` |
| Dispatch ENGINE to fire | `"Engine 2 responding to structure fire, Code 3, all units advised"` |
| Mutual aid request | `"Requesting mutual aid, all local MEDICs committed, Priority 1 cardiac at grid 45-72"` |
| Stage unit | `"Engine 1 staging at District 3 perimeter, awaiting scene clear"` |
"""
readme = readme.replace(
    "| `DOWNGRADE` | Decrease incident severity | New severity must be strictly lower than current |\n",
    "| `DOWNGRADE` | Decrease incident severity | New severity must be strictly lower than current |\n\n" + d1_addition.strip() + "\n"
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)
print("Finished A3 A4 D1.")
