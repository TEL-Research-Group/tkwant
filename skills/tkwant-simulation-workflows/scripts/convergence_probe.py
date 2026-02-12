#!/usr/bin/env python3
"""Quick convergence probe for manybody refinement settings."""

from __future__ import annotations

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare loose and tight manybody refinement tolerances."
    )
    parser.add_argument("--length", type=int, default=5, help="Chain length.")
    parser.add_argument("--tmax", type=float, default=20.0, help="Maximum simulation time.")
    parser.add_argument("--num-times", type=int, default=20, help="Number of time points.")
    parser.add_argument("--rtol-loose", type=float, default=1e-3, help="Loose relative tolerance.")
    parser.add_argument("--atol-loose", type=float, default=1e-3, help="Loose absolute tolerance.")
    parser.add_argument("--rtol-tight", type=float, default=3e-4, help="Tight relative tolerance.")
    parser.add_argument("--atol-tight", type=float, default=3e-4, help="Tight absolute tolerance.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=1e-2,
        help="Fail if max |tight-loose| exceeds this value.",
    )
    return parser.parse_args()


def v(time: float, tau: float = 8.0) -> float:
    if time < tau:
        return time / tau
    return 1.0


def make_system(length: int, kwant):
    def onsite_potential(site, time):
        return 1 + v(time)

    lat = kwant.lattice.square(a=1, norbs=1)
    syst = kwant.Builder()
    syst[(lat(x, 0) for x in range(length))] = 1
    syst[lat.neighbors()] = -1
    syst[lat(0, 0)] = onsite_potential

    sym = kwant.TranslationalSymmetry((-1, 0))
    lead_left = kwant.Builder(sym)
    lead_left[lat(0, 0)] = 1
    lead_left[lat.neighbors()] = -1
    syst.attach_lead(lead_left)
    syst.attach_lead(lead_left.reversed())
    return syst.finalized()


def run_density_trace(syst, times, rtol: float, atol: float, kwant, tkwant, np):
    density_op = kwant.operator.Density(syst)
    state = tkwant.manybody.State(syst, tmax=float(times[-1]))
    traces = []
    for time in times:
        state.evolve(float(time))
        state.refine_intervals(rtol=rtol, atol=atol)
        traces.append(np.asarray(state.evaluate(density_op), dtype=float))
    return np.asarray(traces)


def main() -> int:
    args = parse_args()

    import kwant
    import numpy as np
    import tkwant

    times = np.linspace(0, args.tmax, args.num_times)
    syst = make_system(args.length, kwant)

    loose = run_density_trace(syst, times, args.rtol_loose, args.atol_loose, kwant, tkwant, np)
    tight = run_density_trace(syst, times, args.rtol_tight, args.atol_tight, kwant, tkwant, np)

    max_diff = float(np.max(np.abs(tight - loose)))
    print(f"max_abs_density_diff={max_diff:.6e}")
    print(f"threshold={args.threshold:.6e}")
    if max_diff > args.threshold:
        print("status=FAIL")
        return 1

    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
