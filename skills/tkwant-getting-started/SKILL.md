---
name: tkwant-getting-started
description: This skill should be used when users ask about getting started in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Getting Started

## High-Signal Playbook

### Route the request
- If the question is about installation/import errors, route to `tkwant-build-and-install`.
- If the user asks about boundary conditions or bound states, route to `tkwant-inputs-and-modeling`.
- If the issue is runtime, MPI, or convergence, route to `tkwant-simulation-workflows`.

### Triage questions
- Is the model an open system with leads or a closed finite system?
- Is the user solving a many-body problem (`tkwant.manybody.State`) or a one-body problem?
- Which observable is needed (density, current, Green function)?
- What is the target time window (`tmax`) and number of evaluation times?
- Is the run serial or MPI-parallel?

### Canonical workflow
1. Start from the minimal one-dimensional chain setup in `doc/tutorial_source/getting_started.rst`.
2. Build and finalize a small Kwant system with a single explicit time-dependent perturbation (`doc/tutorial_source/1d_wire_onsite.py`).
3. Define one observable with Kwant operators (density or current).
4. Initialize `tkwant.manybody.State(syst, tmax=...)`.
5. Evolve over time and call `state.refine_intervals(...)` before evaluating observables.
6. Check `state.estimate_error()` and rerun with tighter tolerances if the result changes.
7. Only then scale up size/time or move to advanced tutorials (`doc/tutorial_source/introduction.rst`).

### Minimal working examples
```python
import numpy as np
import kwant
import tkwant

syst = create_system(length=5).finalized()
times = np.linspace(0, 20, 50)
density_op = kwant.operator.Density(syst)
state = tkwant.manybody.State(syst, tmax=max(times))

densities = []
for time in times:
    state.evolve(time)
    state.refine_intervals(rtol=1e-3, atol=1e-3)
    densities.append(state.evaluate(density_op))
```

```python
occup_left = tkwant.manybody.lead_occupation(chemical_potential=0.5, temperature=0.1)
occup_right = tkwant.manybody.lead_occupation(chemical_potential=0.2)
state = tkwant.manybody.State(syst, tmax=20, occupations=[occup_left, occup_right])
```

### Pitfalls
- Skipping `refine_intervals()` can produce non-converged many-body integrals (`doc/tutorial_source/getting_started.rst`, `doc/tutorial_source/pitfalls.rst`).
- Zero-temperature default occupation assumes `mu=0`; no open modes below `mu` can trigger shape/index errors (`doc/tutorial_source/faq.rst`).
- Bound states are not added automatically; ignoring them can bias densities (`doc/tutorial_source/boundstates.rst`).
- Running MPI scripts without root-rank guards duplicates output and can produce `None` on non-root ranks (`doc/tutorial_source/mpi.rst`, `doc/tutorial_source/faq.rst`).
- Ignoring logger warnings hides actionable diagnostics (`doc/tutorial_source/logging.rst`).

### Convergence/validation checklist
- Tighten `rtol`/`atol` in `refine_intervals` and confirm observable changes are negligible.
- Re-evaluate with a denser time grid and verify stable trends.
- Check `state.estimate_error()` at representative times.
- Compare long-time behavior against known benchmarks when available (`doc/tutorial_source/chem_vs_elec_bias.rst`).

## Scope
- Handle questions about initial setup, quickstarts, and core concepts.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/tutorial_source/introduction.rst`
- `doc/tutorial_source/self_consistent.rst`
- `doc/tutorial_source/green_functions.rst`
- `doc/tutorial_source/getting_started.rst`

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
- `tkwant/greenfunctions.py`
- `tkwant/__init__.py`
- `tkwant/system.py`
- `tkwant/special.py`
- `tkwant/mpi.py`
- `tkwant/manybody.py`
- `tkwant/line_segment.py`
- `tkwant/leads.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
