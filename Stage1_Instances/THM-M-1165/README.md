# THM-M-1165 rev-5.6 intake

This `planned` instance covers **Eigenfunction expansion** (`特征函数展开`). The catalogue supplies
only “an eigenfunction representation of a Green function.” That phrase does not determine a
single proposition: the operator, spectrum, boundary conditions, normalization, convergence mode,
and treatment of zero spectrum all change the claim. Intake therefore preserves the intended
subject while refusing to substitute a convenient spectral theorem.

## Scope map

| Surface | Catalogue scope | Intake boundary |
|---|---|---|
| Identity | Eigenfunction representation of a Green function | Preserved as the source-disambiguation target |
| Operator | Presumably a self-adjoint differential operator | Operator, realization, and coefficient assumptions remain open |
| Geometry | Domain/manifold and boundary conditions | Dimension, regularity, compactness, and boundary realization remain open |
| Spectral data | Eigenvalues and eigenfunctions | Discrete-spectrum, multiplicity, basis, and normalization conventions remain open |
| Equality notion | A kernel expansion such as a sum of rank-one terms divided by eigenvalues | Pointwise, almost-everywhere, distributional, operator, or norm convergence is not selected |
| Exceptional cases | Zero modes and spectral parameter | Invertibility, projection off the kernel, or resolvent shift must be fixed by a source |
| Neighbor boundary | Green-function PDE family | Symmetry is `THM-M-1164`; this target must not be replaced by symmetry alone |
| Lean surface | Exact proposition over pinned spectral/measure/PDE APIs | No module or declaration can truthfully be selected yet |

The structured record is `intake.json`; `source_statement_crosswalk.md` records the evidence gap;
and `task_dag.json` gives the open follow-up order.

## Intake verdict

Lifecycle remains `planned`, with provisional root vector `[H5, M4, R4]`. The first failed gate is
exact source-statement identification. No Lean elaboration, proof, or theorem completion is claimed.
