---
name: tkwant-inputs-and-modeling
description: This skill should be used when users ask about inputs and modeling in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Inputs and Modeling

## High-Signal Playbook

### Route the request
- If the question is solver execution/MPI/convergence, route to `tkwant-simulation-workflows`.
- If the user asks for end-to-end runnable scripts, route to `tkwant-examples-and-tutorials`.
- If the question is class/function signatures, route to `tkwant-api-and-scripting`.

### Triage questions
- Is the system open (with leads) or closed (finite)?
- Is time dependence in onsite terms, hoppings, or lead voltages?
- What simulation horizon `tmax` must boundary conditions support?
- Are relevant energy windows known (`emin`, `emax`)?
- Are bound states expected, and must they contribute to observables?
- Is the user using high-level (`State`/`ScatteringStates`) or low-level (`WaveFunction`) APIs?

### Canonical workflow
1. Build and finalize the Kwant system with explicit modeling choices (`doc/tutorial_source/onebody.rst`).
2. Add time dependence through onsite/hopping functions or `tkwant.leads.add_voltage` (`doc/source/reference/tkwant.leads.rst`).
3. For open systems, construct boundary conditions with `automatic_boundary(..., tmax, refl_max, emin, emax)` (`doc/tutorial_source/boundary_condition.rst`).
4. For low-level one-body solves, pass precalculated boundaries explicitly (`doc/tutorial_source/onebody_advanced.rst`).
5. Check bound-state presence using `tkwant.manybody.boundstates_present(syst)` and add them when needed (`doc/tutorial_source/boundstates.rst`).
6. Run a small model first, then tune boundary/reflection parameters and scaling.

### Minimal working examples
```python
import tkwant

boundaries = tkwant.leads.automatic_boundary(
    syst.leads, tmax=10000, refl_max=1e-10, emin=0, emax=1
)
psi = tkwant.onebody.ScatteringStates(
    syst, energy=1.0, lead=0, boundaries=boundaries
)[0]
```

```python
if tkwant.manybody.boundstates_present(syst):
    state.add_boundstate(psi_bs, bs_energy)
```

### Pitfalls
- Forgetting boundaries for open-system low-level one-body workflows (`doc/tutorial_source/onebody_advanced.rst`).
- Choosing `tmax` too small for boundary construction in long simulations (`doc/tutorial_source/boundary_condition.rst`).
- Omitting `emin`/`emax` when a restricted energy window is known, causing avoidable overhead (`doc/tutorial_source/boundary_condition.rst`).
- Ignoring bound states in density calculations (`doc/tutorial_source/boundstates.rst`, `doc/tutorial_source/pitfalls.rst`).
- Confusing electrical-potential and chemical-potential bias modeling (`doc/tutorial_source/chem_vs_elec_bias.rst`).
- Not inspecting lead spectrum/occupied bands before setting occupations (`doc/tutorial_source/pitfalls.rst`, `doc/tutorial_source/manybody.rst`).

### Convergence/validation checklist
- Tighten boundary reflection target (`refl_max`) and verify observables are stable.
- Compare automatic and manual boundary setups for one representative case (`doc/tutorial_source/boundary_condition.rst`).
- Validate full-filling density checks near impurities when bound states are possible (`doc/tutorial_source/boundstates.rst`).
- Recompute with adjusted lead occupations/energy cutoffs to ensure physical consistency (`doc/tutorial_source/manybody.rst`).

## Scope
- Handle questions about inputs, system setup, models, and physical parameterization.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/tutorial_source/boundstates.rst`
- `doc/tutorial_source/boundary_condition.rst`
- `doc/tutorial_source/onebody_advanced.rst`
- `doc/source/reference/tkwant.leads.rst`
- `doc/tutorial_source/alternative_boundary_conditions.rst`

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
- `tkwant/leads.py`
- `tkwant/onebody/__init__.py`
- `tkwant/onebody/solvers.pyx`
- `tkwant/onebody/onebody.py`
- `tkwant/onebody/kernels.pyx`
- `tkwant/onebody/kernels.pxd`
- `tkwant/__init__.py`
- `tkwant/system.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
