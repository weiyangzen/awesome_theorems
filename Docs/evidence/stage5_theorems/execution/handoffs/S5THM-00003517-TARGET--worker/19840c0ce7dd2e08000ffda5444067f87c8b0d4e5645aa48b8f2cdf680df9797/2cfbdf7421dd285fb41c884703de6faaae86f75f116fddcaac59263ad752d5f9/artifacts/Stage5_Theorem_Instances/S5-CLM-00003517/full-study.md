# Full study — epsilon-light subsets

## Frozen claim

For every finite simple graph and every `0 < ε < 1`, there is a subset whose
induced Laplacian is dominated by `ε` times the original Laplacian and whose
cardinality is at least a positive constant times `ε n`.  The source record is
`Arxiv.«2602.05192».epsilon_light_subset_exists`; the target constant supplied
by the constructive proof is `1/256`.

## Reconstruction

The zero-dimensional case is discharged by finite-type elimination.  For fewer
than four vertices, a singleton has zero internal Laplacian, hence is light;
the cast inequality is immediate.  In the large case, the graph Laplacian is a
positive semidefinite Hermitian matrix.  Spectral calculus supplies a square
root and a Moore–Penrose inverse.  Each edge contribution is normalized by the
inverse square root.  The dynamic coloring process maintains a monochromatic
sum under a moving one-sided barrier.  At each step, the sum of all candidate
increments is bounded by the identity in Loewner order.  Trace averaging and
the barrier-potential decrease therefore produce a good vertex/color pair.
After `k = floor(n/4)` steps, every color class pulls back to an ε-light
induced Laplacian.  With `r = ceil(16/ε)` colors, the largest class has size at
least `k/r`; the elementary bounds `n ≤ 8k` and `εr ≤ 32` yield
`k/r ≥ ε n/256`.

## Exceptional cases and trust boundaries

The strict source hypothesis is `ε < 1`; the auxiliary construction is stated
for `ε ≤ 1`, so the target hypothesis supplies it.  Empty and small finite
types are handled before division by the cardinality.  All matrix arguments
are finite-dimensional PSD/Loewner arguments.  The source provider declaration
is explicitly sorry-backed; its bytes are statement authority only.  The task
Lean surfaces perform exact qualified transport and the Master must independently
recompute proof closure before acceptance.

## Formal anchors and downstream uses

The root machine anchor is `audited_root` in `Audit.lean`; the human anchors are
the numbered proof units in `proof-units.json`.  Downstream release uses the
semantic crosswalk, machine closure, readable reverse ledger, current trace,
and strict-dominance certificate.  Deleting any boundary case, arithmetic
inequality, source binding, or trust declaration would invalidate the study.
