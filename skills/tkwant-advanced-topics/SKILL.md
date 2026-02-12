---
name: tkwant-advanced-topics
description: This skill should be used for low-volume tkwant documentation topics that do not justify standalone skills, with docs-first routing before source inspection.
---

# tkwant: Advanced and Specialized Topics

## Scope
- Handle specialized or low-volume topics consolidated from one-doc skills.
- Current consolidated docs are `doc/source/index.rst` and `doc/source/extensions/index.rst`.

## Route the request
- If the question is about installation/build/testing commands, route to `tkwant-build-and-install`.
- If it is about tutorials or runnable examples, route to `tkwant-examples-and-tutorials`.
- If it is about solver settings, boundary conditions, or bound states, route to `tkwant-inputs-and-modeling`.
- If it is about MPI execution and runtime diagnostics, route to `tkwant-simulation-workflows`.

## Primary documentation references
- `doc/source/index.rst`
- `doc/source/extensions/index.rst`

## Workflow
- Start from the primary references above.
- If details are missing, inspect `references/doc_map.md` for the complete topic inventory.
- Only inspect source files via `references/source_map.md` if documentation does not answer the question.
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
- `tkwant/__init__.py`
- `tkwant/system.py`
- `tkwant/leads.py`
- `tkwant/manybody.py`
- `tkwant/onebody/onebody.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
