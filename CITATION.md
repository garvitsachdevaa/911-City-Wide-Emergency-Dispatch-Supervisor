# Citation

If you use 911 Dispatch Supervisor in your research, please cite:

```bibtex
@software{dispatch_supervisor_2025,
  title  = {911 Dispatch Supervisor: An Open RL Benchmark for Emergency Dispatch Decision-Making},
  year   = {2025},
  url    = {https://huggingface.co/spaces/garvitsachdeva/911},
  note   = {OpenEnv-compatible environment for training and evaluating LLM agents
            on real-world emergency resource allocation under time pressure}
}
```

## Research Applications

This environment is designed to support research in:

- LLM decision-making under constraint — fixed action budgets, time pressure
- Multi-objective RL — non-sparse rewards with competing components
- AI safety evaluation — hard constraints (Safety Gate) that cannot be gamed
- Human-AI collaboration — dispatch copilot systems for public safety

## Dataset & Reproducibility

All episodes are fully deterministic under seed=42. The random agent baseline
produces identical scores on every run, enabling valid cross-environment comparisons.
