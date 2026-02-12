---
name: tkwant-build-and-install
description: This skill should be used when users ask about build and install in tkwant; it prioritizes documentation references and then source inspection only for unresolved details.
---

# tkwant: Build and Install

## High-Signal Playbook

### Route the request
- If the issue is runtime/MPI behavior after successful install, route to `tkwant-simulation-workflows`.
- If the user needs runnable physics examples after install, route to `tkwant-examples-and-tutorials`.
- If the question is API usage rather than environment setup, route to `tkwant-api-and-scripting`.

### Triage questions
- Does the user need a packaged install (`conda`/`apt`) or a development build from source?
- Which OS and Python version are being used?
- Are compiler/MPI/Kwant dependencies already installed?
- Is the goal to run tests, build docs, or only import `tkwant`?
- Is the import failing only outside the repository (Python path issue)?

### Canonical workflow
1. Prefer packaged installation first (`conda` or Ubuntu package) from `INSTALL.rst`.
2. For source/development workflows, install Python and non-Python build dependencies listed in `INSTALL.rst`.
3. Build extensions in-place with `python3 setup.py build_ext -i`.
4. Verify `import tkwant` in the target Python environment.
5. Run smoke tests (`pytest`) and then optional MPI/integration tests.
6. Run `skills/tkwant-simulation-workflows/scripts/preflight.py` to validate imports and tutorial script availability.
7. Build docs (`doc/Makefile`) only after runtime environment is stable.
8. For path issues, ensure the package location/symlink is in `site-packages` (`INSTALL.rst`, `doc/tutorial_source/faq.rst`).

### Minimal working examples
```bash
conda install tkwant -c conda-forge
python3 -c "import tkwant; print(tkwant.__version__)"
```

```bash
git clone https://gitlab.kwant-project.org/kwant/tkwant.git
cd tkwant
python3 -m pip install --user cython numpy scipy sympy mpi4py tinyarray kwantspectrum
python3 setup.py build_ext -i
pytest
```

### Pitfalls
- Running tests before compiling extension modules for source builds (`INSTALL.rst`).
- `ModuleNotFoundError` outside repo due to missing/incorrect Python path or symlink (`doc/tutorial_source/faq.rst`).
- Missing MPI/Kwant/toolchain dependencies for source builds (`INSTALL.rst`).
- Mixing Python executables between build and run steps.
- Forgetting extra deps for docs/tests (`README.rst`, `INSTALL.rst`).
- MPI runs failing because thread count is not constrained (`export OMP_NUM_THREADS=1`, `doc/tutorial_source/mpi.rst`, `doc/tutorial_source/faq.rst`).

### Convergence/validation checklist
- Confirm `python3 -c "import tkwant"` works from inside and outside the repository.
- Run `pytest` and at least one MPI test target (`pytest --mpitest`) when MPI is required (`README.rst`).
- Build documentation with `cd doc && make html` for full environment validation (`README.rst`).
- Execute one tutorial script as a final smoke test using `skills/tkwant-simulation-workflows/scripts/run_tutorial.py`.

## Scope
- Handle questions about build, installation, compilation, and environment setup.
- Keep responses abstract and architectural for large codebases; avoid exhaustive per-function documentation unless requested.

## Primary documentation references
- `doc/source/pre/installation.rst`
- `INSTALL.rst`
- `README.rst`

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
- `tkwant/__init__.py`
- `tkwant/system.py`
- `tkwant/special.py`
- `tkwant/mpi.py`
- `tkwant/manybody.py`
- `tkwant/line_segment.py`
- `tkwant/leads.py`
- `tkwant/interaction.py`
- Prefer targeted source search (for example: `rg -n "<symbol_or_keyword>" tkwant`).
