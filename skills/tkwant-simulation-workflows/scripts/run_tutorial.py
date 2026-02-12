#!/usr/bin/env python3
"""Run a tkwant tutorial script in serial or MPI mode with stable defaults."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute tkwant tutorial scripts with reproducible run settings."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Path to the tkwant repository root (default: current directory).",
    )
    parser.add_argument(
        "--script",
        required=True,
        help=(
            "Script path or tutorial basename. "
            "If basename is given, resolves under doc/tutorial_source/."
        ),
    )
    parser.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable for script execution.",
    )
    parser.add_argument(
        "--mpi-ranks",
        type=int,
        default=0,
        help="MPI rank count. Use 0 for serial execution (default).",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Set MPLBACKEND=Agg to avoid GUI requirements.",
    )
    parser.add_argument(
        "--omp-num-threads",
        default="1",
        help="Set OMP_NUM_THREADS (default: 1).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the command and exit without running it.",
    )
    return parser.parse_args()


def resolve_script(repo_root: Path, script: str) -> Path:
    direct = repo_root / script
    if direct.exists():
        return direct
    tutorial = repo_root / "doc" / "tutorial_source" / script
    if tutorial.exists():
        return tutorial
    raise FileNotFoundError(
        f"cannot resolve script '{script}' under repo root or doc/tutorial_source"
    )


def mpi_launcher() -> str:
    for name in ("mpirun", "mpiexec"):
        if shutil.which(name):
            return name
    raise FileNotFoundError("no MPI launcher found (`mpirun` or `mpiexec`)")


def build_command(args: argparse.Namespace, script: Path) -> list[str]:
    repo_root = args.repo_root.resolve()
    try:
        script_arg = str(script.relative_to(repo_root))
    except ValueError:
        script_arg = str(script)
    command = [args.python, script_arg]
    if args.mpi_ranks > 0:
        launcher = mpi_launcher()
        command = [launcher, "-n", str(args.mpi_ranks), *command]
    return command


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    script = resolve_script(repo_root, args.script)

    env = os.environ.copy()
    if args.omp_num_threads:
        env["OMP_NUM_THREADS"] = args.omp_num_threads
    if args.headless:
        env["MPLBACKEND"] = "Agg"

    command = build_command(args, script)

    print(f"repo_root={repo_root}")
    print(f"script={script.relative_to(repo_root)}")
    print(f"OMP_NUM_THREADS={env.get('OMP_NUM_THREADS')}")
    if args.headless:
        print("MPLBACKEND=Agg")
    print("command:", " ".join(command))

    if args.dry_run:
        return 0

    proc = subprocess.run(command, cwd=repo_root, env=env)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
