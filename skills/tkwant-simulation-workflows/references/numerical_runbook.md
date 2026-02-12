# tkwant numerical simulation runbook

Use this runbook when an agent must execute, validate, and iterate on real tkwant simulations.

## 1) Route by goal
- First runnable many-body example: `doc/tutorial_source/1d_wire_onsite.py`
- Faster many-body pattern with error estimate: `doc/tutorial_source/1d_wire_high_level.py`
- MPI-ready current simulation: `doc/tutorial_source/fabry_perot.py`
- Boundary-condition tuning: `doc/tutorial_source/alternative_boundary_conditions.py`
- Restart/checkpoint pattern: `doc/tutorial_source/restarting.rst`
- Chemical vs electrical bias workflow: `doc/tutorial_source/chem_vs_elec_bias_run_computation.py` and `doc/tutorial_source/chem_vs_elec_bias_plot_results.py`

## 2) Preflight before running
- Run from repository root.
- Validate layout, imports, and scripts:

```bash
python skills/tkwant-simulation-workflows/scripts/preflight.py \
  --repo-root . \
  --tutorial 1d_wire_onsite.py \
  --tutorial fabry_perot.py \
  --check-mpi
```

## 3) Canonical execution commands
- Serial, headless plotting:

```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py \
  --repo-root . \
  --script 1d_wire_onsite.py \
  --headless
```

- MPI execution (enforces `OMP_NUM_THREADS=1` by default):

```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py \
  --repo-root . \
  --script fabry_perot.py \
  --mpi-ranks 8 \
  --headless
```

- Two-stage compute/plot workflow:

```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script chem_vs_elec_bias_run_computation.py --headless
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script chem_vs_elec_bias_plot_results.py --headless
```

## 4) Convergence checks (many-body integral)
- Always include `state.refine_intervals(...)` in time loops.
- Inspect `state.estimate_error()` at representative times.
- Re-run with tighter tolerances and compare observables.
- Use a quick tolerance comparison script:

```bash
python skills/tkwant-simulation-workflows/scripts/convergence_probe.py \
  --rtol-loose 1e-3 --atol-loose 1e-3 \
  --rtol-tight 3e-4 --atol-tight 3e-4 \
  --threshold 1e-2
```

## 5) MPI and I/O invariants
- Gate prints/plots/files to rank 0 using `tkwant.mpi.get_communicator().rank == 0`.
- Expect non-root ranks to hold `None` for many evaluated results.
- Keep `OMP_NUM_THREADS=1` for MPI runs.

## 6) Restart/checkpoint invariants
- Save state with `pickle.dump(...)` after deterministic checkpoints.
- Ensure referenced callables (for example perturbation functions) exist when unpickling.
- Resume by loading the state and continuing `evolve(...)` on new times.

## 7) Common failure signatures
- `ModuleNotFoundError: tkwant` outside repo: build/install and ensure package is on `PYTHONPATH` (`INSTALL.rst`, `doc/tutorial_source/faq.rst`).
- Shape/index errors at `T=0`: no open modes below chemical potential; inspect lead spectrum and occupations (`doc/tutorial_source/faq.rst`, `doc/tutorial_source/getting_started.rst`).
- Simulation stalls in refinement: enable logging and adjust tolerances or simplify regime (`doc/tutorial_source/pitfalls.rst`, `doc/tutorial_source/logging.rst`).
- Empty output under MPI: write files only on root rank (`doc/tutorial_source/mpi.rst`, `doc/tutorial_source/faq.rst`).
