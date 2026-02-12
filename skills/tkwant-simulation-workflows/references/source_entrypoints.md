# Simulation source entrypoints

Use this file only when tutorial/reference docs are insufficient.

## Many-body runtime control
- File: `tkwant/manybody.py`
- Symbols:
  - `State.__init__` (high-level setup)
  - `State.evolve` (time stepping)
  - `State.refine_intervals` (adaptive quadrature refinement)
  - `State.estimate_error` (error estimates)
  - `State.evaluate` (observable evaluation)
  - `lead_occupation` (lead occupation model)
  - `boundstates_present` / `add_boundstates` (bound-state handling)
  - `ManybodyIntegrand` (diagnostic integrand inspection)

## One-body runtime control
- Files: `tkwant/onebody/onebody.py`, `tkwant/onebody/__init__.py`
- Symbols:
  - `ScatteringStates`
  - `WaveFunction.from_kwant`
  - `WaveFunction.evolve`
  - `WaveFunction.evaluate`

## Lead boundary and bias modeling
- File: `tkwant/leads.py`
- Symbols:
  - `automatic_boundary`
  - `SimpleBoundary`
  - `MonomialAbsorbingBoundary`
  - `GenericAbsorbingBoundary`
  - `add_voltage`

## MPI behavior
- File: `tkwant/mpi.py`
- Symbols:
  - `get_communicator`
  - `communicator_init`

## Fast lookup patterns
- `rg -n "class State|def refine_intervals|def estimate_error" tkwant/manybody.py`
- `rg -n "class ScatteringStates|class WaveFunction|def from_kwant" tkwant/onebody`
- `rg -n "def automatic_boundary|def add_voltage" tkwant/leads.py`
- `rg -n "def get_communicator|def communicator_init" tkwant/mpi.py`
