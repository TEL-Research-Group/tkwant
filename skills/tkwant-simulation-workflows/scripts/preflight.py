#!/usr/bin/env python3
"""Preflight checks for running local tkwant tutorial simulations."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate local environment and files before running tkwant tutorials."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the tkwant repository root (default: current directory).",
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable used for import checks.",
    )
    parser.add_argument(
        "--tutorial",
        action="append",
        default=[],
        help=(
            "Tutorial script to check. Accepts basename (e.g. fabry_perot.py) "
            "or a repo-relative path. Can be passed multiple times."
        ),
    )
    parser.add_argument(
        "--skip-import-check",
        action="store_true",
        help="Skip checking `import tkwant` and `import kwant`.",
    )
    parser.add_argument(
        "--check-mpi",
        action="store_true",
        help="Check availability of `mpirun` or `mpiexec`.",
    )
    return parser.parse_args()


def resolve_tutorial_path(repo_root: Path, raw: str) -> Path:
    candidate = repo_root / raw
    if candidate.exists():
        return candidate
    tutorial_candidate = repo_root / "doc" / "tutorial_source" / raw
    if tutorial_candidate.exists():
        return tutorial_candidate
    raise FileNotFoundError(raw)


def check_repo_layout(repo_root: Path) -> list[str]:
    issues: list[str] = []
    required = [repo_root / "tkwant", repo_root / "doc" / "tutorial_source", repo_root / "setup.py"]
    for path in required:
        if not path.exists():
            issues.append(f"missing required path: {path}")
    return issues


def check_imports(repo_root: Path, python_exe: str) -> list[str]:
    cmd = [
        python_exe,
        "-c",
        "import tkwant, kwant; print('tkwant', tkwant.__version__)",
    ]
    proc = subprocess.run(cmd, cwd=repo_root, capture_output=True, text=True)
    if proc.returncode == 0:
        return []
    message = proc.stderr.strip() or proc.stdout.strip() or "unknown import failure"
    return [f"python import check failed: {message}"]


def check_mpi() -> list[str]:
    if shutil.which("mpirun") or shutil.which("mpiexec"):
        return []
    return ["MPI launcher not found (`mpirun` or `mpiexec`)."]


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()

    errors: list[str] = []
    notes: list[str] = []

    errors.extend(check_repo_layout(repo_root))

    for tutorial in args.tutorial:
        try:
            path = resolve_tutorial_path(repo_root, tutorial)
            notes.append(f"tutorial found: {path.relative_to(repo_root)}")
        except FileNotFoundError:
            errors.append(f"tutorial not found: {tutorial}")

    if args.check_mpi:
        errors.extend(check_mpi())

    if not args.skip_import_check:
        errors.extend(check_imports(repo_root, args.python))

    print(f"repo_root={repo_root}")
    for note in notes:
        print(f"OK: {note}")

    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        return 1

    print("Preflight checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
