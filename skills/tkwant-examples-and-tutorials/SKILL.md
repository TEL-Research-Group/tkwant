---
name: tkwant-examples-and-tutorials
description: This skill should be used when users ask about examples and tutorials in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Examples and Tutorials

## High-Signal Playbook

### Route the request
- If the user asks for environment setup before running examples, route to `tkwant-build-and-install`.
- If the user asks why an example is numerically unstable/slow, route to `tkwant-simulation-workflows`.
- If the question is about boundary tuning or bound states behind an example, route to `tkwant-inputs-and-modeling`.
- If the request requires deterministic serial/MPI execution commands, load `tkwant-simulation-workflows` and use its bundled scripts.

### Triage questions
- Which tutorial scenario is closest to the user’s target physics?
- Is the request one-body, many-body, or self-consistent?
- Does the user need a quick visual demo or production-quality convergence?
- Should the run be serial or MPI-parallel?
- Does the user need restart/checkpoint behavior?

### Canonical workflow
1. Pick the nearest tutorial from `doc/source/tutorial/index.rst` and `doc/tutorial_source/examples.rst`.
2. Run the original script unmodified first (`doc/tutorial_source/*.py`) using `skills/tkwant-simulation-workflows/scripts/run_tutorial.py`.
3. Validate expected qualitative behavior against the documented narrative/figures.
4. Only then adapt one parameter block at a time.
5. For heavy workflows, switch to MPI and root-rank output guards (`doc/tutorial_source/mpi.rst`).
6. For multi-stage examples, run compute and plot scripts in the intended order (`doc/tutorial_source/chem_vs_elec_bias_run_computation.py`).
7. Add restart logic (`pickle`) when long runs require checkpointing (`doc/tutorial_source/restarting.rst`).

### Minimal working examples
```bash
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script 1d_wire_onsite.py --headless
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script fabry_perot.py --mpi-ranks 8 --headless
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script chem_vs_elec_bias_run_computation.py --headless
python skills/tkwant-simulation-workflows/scripts/run_tutorial.py --script chem_vs_elec_bias_plot_results.py --headless
```

```python
import pickle

pickle.dump((psi, times, current, current_operator), open("state.npy", "wb"))
psi, times, current, current_operator = pickle.load(open("state.npy", "rb"))
```

### Pitfalls
- Running computationally heavy examples in serial mode when MPI is expected (`doc/tutorial_source/manybody.rst`, `doc/tutorial_source/mpi.rst`).
- Forgetting the second plotting step in two-script tutorials (`doc/tutorial_source/chem_vs_elec_bias_run_computation.py`).
- Modifying several parameters at once and losing traceability.
- Missing helper function definitions required by pickle-restored states (`doc/tutorial_source/restarting.rst`).
- Saving/plotting from non-root MPI ranks (`doc/tutorial_source/faq.rst`, `doc/tutorial_source/mpi.rst`).
- Assuming every tutorial is low-cost; some are intentionally long-running (`doc/tutorial_source/manybody.rst`).

### Convergence/validation checklist
- Re-run with tighter `refine_intervals` tolerances and compare outputs.
- Check qualitative agreement with tutorial figures and described limits.
- Repeat with slightly different discretization/time grids and confirm stable trends.
- Compare long-time behavior with known steady-state predictions when available (`doc/tutorial_source/chem_vs_elec_bias.rst`).

## Scope
- Handle questions about worked examples, tutorials, and cookbook usage.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/source/tutorial/index.rst`
- `doc/tutorial_source/manybody_advanced.rst`
- `doc/tutorial_source/onebody.rst`
- `doc/tutorial_source/logging.rst`
- `doc/tutorial_source/manybody.rst`
- `doc/tutorial_source/time_dep_system.rst`
- `doc/tutorial_source/voltage_raise.rst`
- `doc/tutorial_source/open_system.rst`
- `doc/tutorial_source/graphene.rst`
- `doc/tutorial_source/fabry_perot.rst`
- `doc/tutorial_source/closed_system.rst`
- `doc/tutorial_source/restarting.rst`

## Workflow
- Start with the primary references above.
- If details are missing, inspect `references/doc_map.md` for the complete topic document list.
- Use tutorials/examples as executable usage patterns when available.
- Use tests as behavior or regression references when available.
- If ambiguity remains after docs, inspect `references/source_map.md` and start with the ranked source entry points.
- Cite exact documentation file paths in responses.

## Tutorials and examples
- `doc/tutorial_source`
- `doc/source/tutorial`

## Test references
- `tkwant/tests`
- `tkwant/onebody/tests`

## Optional deeper inspection
- `tkwant`

## Source entry points for unresolved issues
- `tkwant/system.py`
- `tkwant/manybody.py`
- `tkwant/_logging.py`
- `tkwant/onebody/__init__.py`
- `tkwant/onebody/solvers.pyx`
- `tkwant/onebody/onebody.py`
- `tkwant/onebody/kernels.pyx`
- `tkwant/onebody/kernels.pxd`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
