---
name: tkwant-pitfalls
description: Diagnose and fix common tkwant simulation pitfalls from the "Frequent pitfalls encountered when doing Tkwant simulations" tutorial, including many-body integral convergence, bound-state omissions, Hamiltonian/occupation mistakes, observable index mapping, perturbation interpolation accuracy, lead reflections, and time-stepping accuracy. Use when results look wrong, unstable, or unexpectedly slow.
---

# tkwant: Pitfalls and Diagnostics

## High-Signal Playbook

### Route the request
- Route installation/build/import failures to `tkwant-build-and-install`.
- Route full execution orchestration (serial/MPI commands, restarts, runbooks) to `tkwant-simulation-workflows`.
- Route API signature lookups to `tkwant-api-and-scripting`.
- Keep this skill focused on root-cause diagnosis when a simulation runs but results are suspicious.

### Triage questions
- Is the issue many-body convergence, one-body time integration, or model construction?
- Does the run stall in `refine_intervals()`?
- Are bound states present but not included?
- Are occupations physically consistent with the lead band structure and chemical potential?
- Could result interpretation be an observable indexing issue?
- Is the perturbation strongly time-varying (`W(t)`), making interpolation risky?

### Canonical diagnostic workflow
1. Enable logging early (`tkwant.logging.level = logging.INFO`) and scan warnings.
2. Re-check many-body convergence with tighter `refine_intervals(...)` and `estimate_error()`.
3. If refinement stalls, inspect the integrand shape with `tkwant.manybody.ManybodyIntegrand`.
4. Check for unincluded bound states with `tkwant.manybody.boundstates_present(...)`.
5. Validate Hamiltonian physics: plot system and lead band structure; confirm occupied modes exist below `mu`.
6. Validate observable index mapping with `tkwant.system.siteId(...)` before interpreting arrays.
7. For abrupt perturbations, rerun with interpolation disabled and compare outputs.
8. Check lead-reflection sensitivity by rerunning with stricter boundary settings.
9. Check one-body time-stepping sensitivity by rerunning with tighter solver tolerances.

### Pitfall matrix (from pitfalls tutorial)
- Many-body integral under-resolved: run adaptive refinement repeatedly and compare observables (`doc/tutorial_source/pitfalls.rst`, `doc/tutorial_source/manybody.rst`).
- Many-body refinement stalls: inspect problematic intervals/integrand; simplify physics regime if needed (`doc/tutorial_source/pitfalls.rst`).
- Unincluded bound states: detect and include bound-state contributions (`doc/tutorial_source/boundstates.rst`, `doc/tutorial_source/pitfalls.rst`).
- Wrong Hamiltonian or unphysical parameters: verify geometry, couplings, and occupied bands (`doc/tutorial_source/pitfalls.rst`, `doc/tutorial_source/manybody_advanced.rst`).
- Observable mapping errors: use `siteId` to map flattened arrays back to lattice positions (`doc/tutorial_source/pitfalls.rst`).
- Perturbation interpolation inaccuracy: compare default interpolated vs exact perturbation extraction (`doc/tutorial_source/onebody_advanced.rst`, `doc/tutorial_source/manybody_advanced.rst`).
- Spurious lead reflections: tighten/inspect boundary conditions and compare (`doc/tutorial_source/boundary_condition.rst`, `doc/tutorial_source/alternative_boundary_conditions.rst`).
- Time-step accuracy issues: tighten one-body solver tolerances and compare (`doc/tutorial_source/onebody_advanced.rst`, `doc/tutorial_source/manybody_advanced.rst`).

### Minimal working snippets
```python
import logging
import tkwant

tkwant.logging.level = logging.INFO
```

```python
state.evolve(time)
state.refine_intervals(rtol=1e-3, atol=1e-3)
err = state.estimate_error()
```

```python
has_boundstates = tkwant.manybody.boundstates_present(syst)
```

```python
idx = tkwant.system.siteId(syst, lat)
site_index = idx(i, j)
```

## Scope
- Diagnose unstable, inaccurate, or suspicious tkwant simulation results using the official pitfalls guidance.
- Prioritize reproducible rerun-and-compare checks before deep source inspection.
- Use `doc/tutorial_source/pitfalls.rst` as the local source for the stable docs page `https://tkwant.kwant-project.org/doc/stable/tutorial/pitfalls.html`.

## Primary documentation references
- `doc/tutorial_source/pitfalls.rst`
- `doc/tutorial_source/logging.rst`
- `doc/tutorial_source/boundstates.rst`
- `doc/tutorial_source/manybody.rst`
- `doc/tutorial_source/onebody_advanced.rst`
- `doc/tutorial_source/manybody_advanced.rst`
- `doc/tutorial_source/boundary_condition.rst`
- `doc/tutorial_source/faq.rst`

## Workflow
- Start from the primary references above.
- If details are missing, inspect `references/doc_map.md` for the complete topic document list.
- Follow compare-against-baseline diagnostics before changing multiple controls at once.
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
- `tkwant/manybody.py`
- `tkwant/system.py`
- `tkwant/leads.py`
- `tkwant/onebody/onebody.py`
- `tkwant/onebody/solvers.pyx`
- `tkwant/onebody/kernels.pyx`
- `tkwant/_logging.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
