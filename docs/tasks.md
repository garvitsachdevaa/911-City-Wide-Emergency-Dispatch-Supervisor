# Task Reference — 911 Dispatch Supervisor

## Task 1: `single_incident` — Easy

**Objective:** Dispatch the correct unit to a single cardiac arrest and resolve it
before the survival clock expires.

**Initial State:** 1 incident (cardiac arrest, P1), 3 units available (1 MEDIC, 1 ENGINE, 1 PATROL)
**Max Steps:** 20 | **Survival Clock:** 600s

**What a good agent does:** Immediately dispatches MEDIC to the cardiac arrest.
Does not dispatch ENGINE or PATROL (triage mismatch penalty).

**What a bad agent does:** Dispatches ENGINE (wrong unit type), wastes steps,
patient survival clock expires → Safety Gate → score capped at 0.2.

**Scoring:** 50% resolution + 30% correct unit type + 20% response speed

---

## Task 2: `multi_incident` — Medium

**Objective:** Triage 3 simultaneous incidents with competing priorities.

**Initial State:** 3 incidents (structure fire P2, cardiac arrest P1, shooting P1),
6 units available
**Max Steps:** 40

**What a good agent does:** Immediately dispatches MEDIC to cardiac arrest and
PATROL to shooting (both P1), then dispatches ENGINE to structure fire (P2).

**What a bad agent does:** Dispatches to the fire first (visible/dramatic but P2),
leaving P1 incidents unattended → Safety Gate.

**Scoring:** 50% P1 resolution + 30% overall resolution − 20% escalation penalty

---

## Task 3: `mass_casualty` — Hard

**Objective:** Manage a building collapse with surprise incident waves.

**Initial State:** 1 incident (building collapse P1, survival 480s), 7 units
**Max Steps:** 60
**Wave spawns:** Step 5 → structure fire; Step 12 → 2× cardiac arrests

**What a good agent does:** Responds to building collapse immediately, pre-stages
units for anticipated waves, adapts when cardiac arrests spawn at step 12.

**What a bad agent does:** Commits all units to building collapse, has no
available units when cardiac arrests spawn → multiple P1 failures → Safety Gate.

**Scoring:** 60% P1 survival + 30% mean step reward − failure penalty

---

## Task 4: `shift_surge` — Hard

**Objective:** Maintain coverage as units go out of service mid-shift.

**Initial State:** 5 units, 0 incidents (board starts empty)
**Max Steps:** 60 | **Wave spawn:** Every 8 steps | **Survival clock:** 720s
**OOS events:** 3 units go OUT_OF_SERVICE by step 5

**What a good agent does:** Anticipates resource scarcity, requests mutual aid
early, stages remaining units strategically, prioritizes P1 incidents as board fills.

**What a bad agent does:** Dispatches all units freely in early steps, has no
coverage when OOS events hit and new incidents spawn simultaneously.

**Scoring:** 35% resolution + 25% P1 survival + 15% coverage + 15% backlog +
10% step reward − 25% escalation penalty
