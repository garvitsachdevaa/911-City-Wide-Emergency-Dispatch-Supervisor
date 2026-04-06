# Remaining Changes Needed — 911 Dispatch Supervisor (as of 2026-04-06)

This file lists ONLY the work still required to fully match the hackathon requirements provided (OpenAI client + OPENAI_API_KEY baseline, HF Spaces readiness, and portable validation tooling). Items already implemented (OpenEnv YAML, tasks/graders, reward shaping, Docker boot, /reset {} support, etc.) are intentionally omitted.

---

## SECTION 1 — BASELINE INFERENCE MUST USE OPENAI CLIENT + OPENAI_API_KEY (REQUIRED)

### 1.1 Update inference auth variables to match requirement
**Problem:** The requirement explicitly calls for `OPENAI_API_KEY`. Current code requires `HF_TOKEN` and does not recognize `OPENAI_API_KEY`.  
**Where:** [inference.py](inference.py), [README.md](README.md), [validate_local.py](validate_local.py), [tests/test_inference.py](tests/test_inference.py)

**Action:**
- Treat `OPENAI_API_KEY` as the primary credential env var.
- Keep backward-compatible support for `HF_TOKEN` (optional), but do not require it.
- Update README Environment Variables table + examples to show `OPENAI_API_KEY`.

**Verify:**
- `OPENAI_API_KEY=x USE_RANDOM=true API_BASE_URL=https://api.openai.com/v1 MODEL_NAME=gpt-4 uv run python inference.py`
  - Must run and print `[START]` / `[STEP]` / `[END]` lines.

---

### 1.2 Replace hand-rolled HTTPX chat call with the official OpenAI Python client
**Problem:** Requirement says “Uses the OpenAI API client”. Current LLM agent calls `/chat/completions` via HTTPX directly.  
**Where:** [inference.py](inference.py)

**Action:**
- Implement the LLM agent using the `openai` Python package already present in dependencies.
- Continue supporting `API_BASE_URL` + `MODEL_NAME`.
- Ensure output format stays unchanged (tests depend on it).

**Verify:**
- With `USE_RANDOM=false` and a real key, it should complete at least one episode.
- With `USE_RANDOM=true`, it should not require any API key.

---

### 1.3 Update env-var validation tests to reflect OPENAI_API_KEY support
**Problem:** Tests currently set `HF_TOKEN` and never mention `OPENAI_API_KEY`.  
**Where:** [tests/test_inference.py](tests/test_inference.py)

**Action:**
- Update tests to provide `OPENAI_API_KEY` instead of `HF_TOKEN` (or accept either).
- Add/adjust a test that asserts: missing `OPENAI_API_KEY` fails only when `USE_RANDOM != true`.

**Verify:**
- `uv run python -m pytest tests/test_inference.py -q` passes.

---

## SECTION 2 — HF SPACES (DOCKER) READINESS (REQUIRED)

### 2.1 Make server bind to the Hugging Face provided port
**Problem:** HF Docker Spaces typically set `PORT=7860`. Current server binds to port 8000 unconditionally.  
**Where:** [src/server/app.py](src/server/app.py), and Docker entrypoints in [Dockerfile](Dockerfile) + [src/server/Dockerfile](src/server/Dockerfile)

**Action:**
- In the server `main()`, read port from `PORT` env var (default 8000).
- Ensure Docker CMD uses that same port behavior (either via the Python `main()` or uvicorn args).

**Verify:**
- `PORT=7860 uv run python -m src.server.app` listens on 7860.
- `docker run -e PORT=7860 -p 7860:7860 citywide-dispatch-supervisor` works and `/health` responds.

---

### 2.2 Replace README “HF Space Placeholder” with real deploy instructions (or link)
**Problem:** Requirement says “Deploy to Hugging Face Spaces”. README currently has a placeholder only.  
**Where:** [README.md](README.md)

**Action:**
- Add either:
  - A real link to the deployed Space, OR
  - Minimal, accurate deployment steps for creating a Docker Space (with required tags already present).
- Mention expected public URL and what endpoints should work (`/health`, `/reset`, `/step`, `/state`).

**Verify:**
- README no longer contains “Placeholder”.

---

## SECTION 3 — PORTABLE VALIDATION TOOLING (STRONGLY RECOMMENDED)

### 3.1 Ensure `openenv validate` is installable from dependencies
**Problem:** Repo depends on `openenv-core`, but the CLI validator is provided by the `openenv` package. On a clean machine, `openenv validate` may be missing unless `openenv` is a dependency.  
**Where:** [pyproject.toml](pyproject.toml), [requirements.txt](requirements.txt)

**Action:**
- Add `openenv>=0.2.0` (or the current compatible version) to dependencies so `openenv validate` is guaranteed available after install.

**Verify:**
- In a fresh venv after installing dependencies: `uv run openenv validate` succeeds.

---

## SECTION 4 — FINAL SUBMISSION CHECKS (RUN BEFORE SUBMITTING)

Run these in order:

1) `python -c "import yaml; yaml.safe_load(open('openenv.yaml')); print('YAML OK')"`

2) `uv run python -m pytest tests/ -q`

3) Random baseline inference (no API key required):
- `USE_RANDOM=true API_BASE_URL=https://api.openai.com/v1 MODEL_NAME=gpt-4 uv run python inference.py`

4) Local structure validation:
- `uv run openenv validate`

5) Docker sanity:
- `docker build -t citywide-dispatch-supervisor .`
- `docker run -p 8000:8000 citywide-dispatch-supervisor`
- `curl -s http://localhost:8000/health`
- `curl -s -X POST http://localhost:8000/reset -H "Content-Type: application/json" -d '{}'`

All must pass.