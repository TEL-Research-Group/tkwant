---
name: tkwant-api-and-scripting
description: This skill should be used when users ask about api and scripting in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: API and Scripting

## High-Signal Playbook

### Route the request
- If the user primarily needs runnable tutorial code, route to `tkwant-examples-and-tutorials`.
- If the question is model setup (boundaries, bound states, voltages), route to `tkwant-inputs-and-modeling`.
- If the issue is MPI/runtime diagnostics, route to `tkwant-simulation-workflows`.

### Triage questions
- Is this a one-body (`tkwant.onebody`) or many-body (`tkwant.manybody`) problem?
- Is high-level (`State`) or low-level (`WaveFunction`) control needed?
- Are lead occupations custom (different `mu`, `T`, or bands)?
- Is custom perturbation extraction required for stiff/rapid driving?
- Is logging configuration needed for debugging?

### Canonical workflow
1. Use reference landing pages to choose module scope (`doc/source/reference/tkwant.rst`, `doc/source/reference/tkwant.manybody.rst`, `doc/source/reference/tkwant.logging.rst`).
2. Build/finalize the Kwant system and define observable operators.
3. Instantiate occupations with `manybody.lead_occupation(...)` as needed (`doc/tutorial_source/manybody.rst`).
4. Start with high-level `manybody.State` for robust defaults.
5. For advanced control, switch to low-level APIs or custom wavefunction/scattering-state factories (`doc/tutorial_source/manybody_advanced.rst`, `doc/tutorial_source/chem_vs_elec_bias_run_computation.py`).
6. Add logging/filtering only after baseline correctness is established (`doc/tutorial_source/logging.rst`).

### Minimal working examples
```python
import tkwant

occup_left = tkwant.manybody.lead_occupation(chemical_potential=0.5, temperature=0.1)
occup_right = tkwant.manybody.lead_occupation(chemical_potential=0.2)
state = tkwant.manybody.State(syst, tmax=100, occupations=[occup_left, occup_right])
state.evolve(40)
state.refine_intervals(rtol=1e-3, atol=1e-3)
value = state.evaluate(observable)
```

```python
import functools
import tkwant

wavefunction_type = functools.partial(
    tkwant.onebody.WaveFunction.from_kwant,
    perturbation_type=tkwant.onebody.kernels.PerturbationExtractor,
)
scattering_state_type = functools.partial(
    tkwant.onebody.ScatteringStates, wavefunction_type=wavefunction_type
)
state = tkwant.manybody.State(syst, tmax=100, scattering_state_type=scattering_state_type)
```

### Pitfalls
- Choosing low-level APIs before establishing a working high-level baseline.
- Mismatching occupation specification with lead count or band structure (`doc/tutorial_source/manybody.rst`, `doc/tutorial_source/manybody_advanced.rst`).
- Forgetting to pass model parameters (`params`) needed by time-dependent onsite/hopping callbacks (`doc/tutorial_source/chem_vs_elec_bias_run_computation.py`).
- Using `manybody.State` for self-consistent problems that require low-level `manybody.WaveFunction` workflows (`doc/tutorial_source/self_consistent.rst`).
- Setting logging options too late (after simulation work already started) (`doc/tutorial_source/logging.rst`).
- Treating `doc/templates/autosummary/class.rst` as user API documentation instead of Sphinx template infrastructure.

### Convergence/validation checklist
- Validate the same observable with two API pathways (high-level vs low-level) on a small case.
- Check lead occupations and cutoffs produce expected occupied modes.
- For custom perturbation handling, compare against default interpolation on a short run.
- Ensure logger output is informative but not masking runtime behavior changes.

## Scope
- Handle questions about language bindings, APIs, and programmatic interfaces.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/tutorial_source/chem_vs_elec_bias.rst`
- `doc/source/reference/tkwant.manybody.rst`
- `doc/source/reference/tkwant.rst`
- `doc/source/reference/tkwant.logging.rst`
- `doc/templates/autosummary/class.rst`

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
- `tkwant/manybody.py`
- `tkwant/_logging.py`
- `tkwant/greenfunctions.py`
- `tkwant/__init__.py`
- `tkwant/system.py`
- `tkwant/special.py`
- `tkwant/mpi.py`
- `tkwant/line_segment.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
