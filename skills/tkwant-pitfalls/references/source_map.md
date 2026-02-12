# tkwant source map: Pitfalls and Diagnostics

Generated from source roots:
- `tkwant`

Use this map only after exhausting the topic docs in `references/doc_map.md`.

## Topic query tokens
- `pitfall`
- `refine`
- `estimate`
- `integrand`
- `boundstates`
- `occupation`
- `siteid`
- `boundary`
- `reflection`
- `perturbation`
- `interpolation`
- `solver`
- `logging`

## Fast source navigation
- `rg -n "<symbol_or_keyword>" tkwant`
- `rg -n "class|def|struct|namespace" tkwant`
- If a doc mentions a function/class, search that exact symbol first, then inspect nearby implementation files.

## Suggested source entry points
- `tkwant/manybody.py` | score: 10 | matched tokens: refine, estimate, integrand, boundstates, occupation
- `tkwant/system.py` | score: 3 | matched tokens: siteid
- `tkwant/leads.py` | score: 4 | matched tokens: boundary, reflection
- `tkwant/onebody/onebody.py` | score: 4 | matched tokens: perturbation, boundary, solver
- `tkwant/onebody/solvers.pyx` | score: 2 | matched tokens: solver
- `tkwant/onebody/kernels.pyx` | score: 3 | matched tokens: perturbation, interpolation
- `tkwant/_logging.py` | score: 2 | matched tokens: logging
- `tkwant/mpi.py` | fallback entry point
- `tkwant/greenfunctions.py` | fallback entry point
