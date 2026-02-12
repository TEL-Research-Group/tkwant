---
name: tkwant-reference
description: This skill should be used when users ask about reference in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Reference

## Scope
- Handle questions about documentation grouped under the 'reference' theme.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/source/reference/index.rst`
- `doc/source/reference/tkwant.system.rst`
- `doc/source/reference/tkwant.integrate.rst`

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
- `tkwant/__init__.py`
- `tkwant/special.py`
- `tkwant/mpi.py`
- `tkwant/manybody.py`
- `tkwant/line_segment.py`
- `tkwant/leads.py`
- `tkwant/interaction.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
