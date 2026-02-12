---
name: tkwant-index
description: Route tkwant user requests to the right topic skill, with default priority on executable numerical-simulation workflows (preflight, run, converge, MPI, restart) before deep source inspection.
---

# tkwant Skills Index

## Route the request
- Classify the request into one of the generated topic skills listed below.
- For requests that involve running or fixing a simulation, route first to `tkwant-simulation-workflows`.
- For requests focused on suspicious results or numerical artifacts, route to `tkwant-pitfalls`.
- Prefer workflow-level guidance and runnable commands before source-level detail.

## Default simulation-first path
1. `tkwant-build-and-install` for environment/import issues.
2. `tkwant-simulation-workflows` for preflight, execution, convergence, MPI, and restart.
3. `tkwant-pitfalls` for systematic diagnosis of unstable/inaccurate results.
4. `tkwant-inputs-and-modeling` for model/boundary setup changes.
5. `tkwant-api-and-scripting` for API-level customization.

## Generated topic skills
- `tkwant-examples-and-tutorials`: Examples and Tutorials (worked examples, tutorials, and cookbook usage)
- `tkwant-pitfalls`: Pitfalls and Diagnostics (official pitfalls checklist for convergence, bound states, interpolation, boundaries, and observable mapping)
- `tkwant-inputs-and-modeling`: Inputs and Modeling (inputs, system setup, models, and physical parameterization)
- `tkwant-api-and-scripting`: API and Scripting (language bindings, APIs, and programmatic interfaces)
- `tkwant-getting-started`: Getting Started (initial setup, quickstarts, and core concepts)
- `tkwant-simulation-workflows`: Simulation Workflows (simulation setup, execution flow, and runtime controls)
- `tkwant-theory-and-methods`: Theory and Methods (theoretical background and algorithmic methods)
- `tkwant-build-and-install`: Build and Install (build, installation, compilation, and environment setup)
- `tkwant-pre`: Pre (documentation grouped under the 'pre' theme)
- `tkwant-reference`: Reference (documentation grouped under the 'reference' theme)
- `tkwant-advanced-topics`: Advanced and Specialized Topics (consolidated low-volume docs: top-level docs navigation and extensions landing pages)

## Documentation-first inputs
- `doc`

## Tutorials and examples roots
- `doc/tutorial_source`
- `doc/source/tutorial`

## Test roots for behavior checks
- `tkwant/tests`
- `tkwant/onebody/tests`

## Escalate only when needed
- Start from topic skill primary references.
- Prefer bundled workflow scripts from the selected skill when available.
- If those references are insufficient, search the topic skill `references/doc_map.md`.
- If documentation still leaves ambiguity, open `references/source_map.md` inside the same topic skill and inspect the suggested source entry points.
- Use targeted symbol search while inspecting source (e.g., `rg -n "<symbol_or_keyword>" tkwant`).

## Source directories for deeper inspection
- `tkwant`
