---
name: tkwant-theory-and-methods
description: This skill should be used when users ask about theory and methods in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Theory and Methods

## Scope
- Handle questions about theoretical background and algorithmic methods.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/source/reference/tkwant.onebody.rst`
- `doc/source/reference/tkwant.onebody.solvers.rst`
- `doc/source/reference/tkwant.onebody.kernel.rst`

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
- `tkwant/onebody/solvers.pyx`
- `tkwant/onebody/kernels.pyx`
- `tkwant/onebody/kernels.pxd`
- `tkwant/onebody/__init__.py`
- `tkwant/onebody/onebody.py`
- `tkwant/__init__.py`
- `tkwant/system.py`
- `tkwant/special.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
