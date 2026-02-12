---
name: tkwant-simulation-workflows
description: Execute and debug end-to-end tkwant numerical simulations, including serial/MPI runs, convergence control (`refine_intervals`, `estimate_error`), checkpoint/restart, and runtime diagnostics. Use this when the request is about actually running or stabilizing simulations, not only API lookups.
---

# tkwant: Simulation Workflows

## High-Signal Playbook

### Route the request
- Route installation/import failures to `tkwant-build-and-install`.
- Route model and boundary design questions to `tkwant-inputs-and-modeling`.
- Route class-signature or API-only questions to `tkwant-api-and-scripting`.
- Route tutorial selection without execution to `tkwant-examples-and-tutorials`.
- Route checklist-style root-cause diagnosis of suspicious results to `tkwant-pitfalls`.

### Triage questions
- Is the target workflow one-body or many-body?
- Is the run intended to be serial or MPI?
- Is the user asking for first-run smoke validation, production scaling, or debugging?
- Is output guarded to root rank for MPI?
- Are convergence checks (`refine_intervals`, `estimate_error`) already in place?
- Is checkpoint/restart needed for long jobs?

### Enforce invariants
- Run commands from repository root.
- Keep `OMP_NUM_THREADS=1` for MPI executions.
- Restrict print/plot/file writes to MPI root rank.
- Perform at least one tighter-tolerance re-run before trusting results.

### Canonical execution workflow
1. Run preflight checks with `scripts/preflight.py`.
2. Execute a baseline tutorial in serial mode.
3. Confirm convergence behavior with `refine_intervals` and `estimate_error`.
4. Switch to MPI only after serial behavior is validated.
5. Add checkpoint/restart for long simulations.
6. Enable logging (`tkwant.logging.level = logging.INFO`) when refinement or runtime stalls.
7. Escalate to source inspection only if docs and runbook do not resolve the issue.

### Minimal working examples
```bash
python skills/tkwant-simulation-workflows/scripts/preflight.py \
  --repo-root . \
  --tutorial 1d_wire_onsite.py \
  --tutorial fabry_perot.py \
  --check-mpi
```

```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py \
  --repo-root . \
  --script 1d_wire_onsite.py \
  --headless
```

```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py \
  --repo-root . \
  --script fabry_perot.py \
  --mpi-ranks 8 \
  --headless
```

```python
import sys
import tkwant

def am_master():
    return tkwant.mpi.get_communicator().rank == 0

def print_master(*args, **kwargs):
    if am_master():
        print(*args, **kwargs)
    sys.stdout.flush()
```

### Pitfalls
- Running MPI without root-rank output guards duplicates output and can propagate `None` values (`doc/tutorial_source/mpi.rst`, `doc/tutorial_source/faq.rst`).
- Forgetting `OMP_NUM_THREADS=1` degrades or breaks MPI runs (`doc/tutorial_source/mpi.rst`).
- Skipping refinement checks leads to unconverged many-body integrals (`doc/tutorial_source/pitfalls.rst`).
- Over-tight refinement on difficult integrands can stall runtime (`doc/tutorial_source/pitfalls.rst`).
- Omitting callable definitions required by pickle on restart breaks state loading (`doc/tutorial_source/restarting.rst`).
- Ignoring warning/info logs hides convergence and occupation issues (`doc/tutorial_source/logging.rst`).

### Convergence/validation checklist
- Re-run with tighter `refine_intervals` tolerances and compare key observables.
- Check `estimate_error()` at multiple representative times.
- Compare short serial and MPI-root runs for consistent results.
- Validate against tutorial reference behavior where available (`doc/tutorial_source/chem_vs_elec_bias.rst`, `doc/tutorial_source/fabry_perot.rst`).
- Use `scripts/convergence_probe.py` for quick tolerance-difference checks.

## Scope
- Execute and stabilize simulation runs (serial or MPI) with reproducible commands.
- Diagnose convergence/runtime issues with doc-backed procedures before deep source dives.

## Primary documentation references
- `doc/tutorial_source/pitfalls.rst`
- `doc/tutorial_source/mpi.rst`
- `doc/tutorial_source/restarting.rst`
- `doc/tutorial_source/logging.rst`
- `doc/tutorial_source/faq.rst`
- `doc/tutorial_source/manybody.rst`
- `doc/source/reference/tkwant.mpi.rst`

## Workflow
- Start with the primary references above.
- If details are missing, inspect `references/doc_map.md` for the complete topic document list.
- For runnable command patterns, load `references/numerical_runbook.md`.
- For source-level symbol lookup, load `references/source_entrypoints.md`.
- Use tutorials/examples as executable usage patterns when available.
- Use tests as behavior or regression references when available.
- If ambiguity remains after docs, inspect `references/source_map.md` and start with the ranked source entry points.
- Cite exact documentation file paths in responses.

## Bundled scripts
- `scripts/preflight.py`: validate environment, imports, and tutorial file availability.
- `scripts/run_tutorial.py`: run tutorial scripts with serial/MPI options and stable environment defaults.
- `scripts/convergence_probe.py`: compare loose/tight many-body refinement settings.

## Bundled references
- `references/numerical_runbook.md`
- `references/source_entrypoints.md`

## Tutorials and examples
- `doc/tutorial_source`
- `doc/source/tutorial`

## Test references
- `tkwant/tests`
- `tkwant/onebody/tests`

## Optional deeper inspection
- `tkwant`

## Source entry points for unresolved issues
- `tkwant/manybody.py`
- `tkwant/onebody/onebody.py`
- `tkwant/leads.py`
- `tkwant/mpi.py`
- `tkwant/onebody/solvers.pyx`
- `tkwant/system.py`
- `tkwant/__init__.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
