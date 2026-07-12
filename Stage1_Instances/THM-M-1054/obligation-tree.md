# THM-M-1054 obligation tree

Registry `THM-M-1054-OBLIGATIONS-v1` freezes thirteen canonical obligations before proof-node
credit is observed. Proof requirements point from parent to child in `typed-graphs.json`; every
such edge has a reciprocal child-to-parent `composes` edge. The root stays `[H1, M3, R3]`.

## Proof route

`M1054-ROOT` requires `M1054-T-ASSEMBLE`. Assembly splits exhaustively on whether real `L2` is a
subsingleton. The degenerate branch is constant convergence. The nontrivial branch requires the
Koopman construction, its norm bound, and the abstract Hilbert-space mean-ergodic theorem. The
fixed-space transport checks that the abstract projection is exactly the limit named by the root.

The pinned declaration `ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection` is a
feasible terminal candidate, but this phase deliberately records it as open proof-node work. The
conditional Lean composition therefore accepts `NontrivialMeanErgodicPackage` as a premise rather
than importing proof credit from the preceding anchor audit.

## Node index

### m1054-root
Exact real `L2` Koopman convergence proposition. Required machine, human-source, and readable node.

### m1054-s-definitions
The `Lp`, Koopman, Cesaro-average, and orthogonal-projection vocabulary frozen by `Statement.lean`.

### m1054-s-boundary
The checked alias and zero-length average; identity and non-ergodic maps remain in scope.

### m1054-s-foundation
Open transitive axiom, import, TCB, and no-oracle policy certificate.

### m1054-c-koopman
Construction of the composition linear isometry and its continuous linear map.

### m1054-l-contraction
Extraction of the operator-norm bound from the linear-isometry construction.

### m1054-b-subsingleton
Degenerate `L2` branch, where all averages equal the invariant projection.

### m1054-b-nontrivial
Nontrivial Hilbert-space branch consuming the contraction and abstract theorem.

### m1054-l-abstract-mean-ergodic
The root-critical open proof-credit node represented by the pinned mathlib candidate.

### m1054-t-fixed-projection
Transport from the abstract fixed locus to the exact `InvariantProjection` target.

### m1054-t-assemble
Checked conditional composition in `ObligationTree.lean`; it is not a proof of the open package.

### m1054-x-source
Open page-level primary-source, assumptions, conventions, errata, and reviewer crosswalk.

### m1054-x-provenance
Open release overlay for terminal bodies, aliases, imports, axioms, TCB, and replay receipts.

## Boundary

This artifact freezes scope, eligibility, ledgers, and typed graph topology only. It does not claim
the root, source fidelity, readable reconstruction, audit completion, theorem completion, release
reproduction, independent verification, or master acceptance.
