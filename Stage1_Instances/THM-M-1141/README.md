# THM-M-1141 rev-5.6 statement

This remains a fail-closed `planned` dossier for the classical Harnack inequality. The repository
source identifies only "comparison of positive harmonic functions" and Axel Harnack (1887).
`Statement.lean` now freezes the precise compact-subset form in Axler, Bourdon, and Ramey,
*Harmonic Function Theory*, second edition, Theorem 3.6 (page 48 of the numbered text).

For a connected open Euclidean domain `Omega` and compact `K ⊆ Omega`, it asserts the existence
of `C > 1`, independent of the points and strictly positive harmonic function, such that
`1 / C ≤ u y / u x ≤ C` for every `x,y ∈ K`. This is the exact modern-source variant selected
for formal execution; the 1887 historical source remains unaudited and is not credited as H0.

The provisional root vector is `[H1, M3, R3]`. The canonical expression elaborates, but it has no
proof body or accepted proof state. There is no audit completion or theorem completion. The source
label `已验证` remains untrusted metadata and supplies no rev-5.6 proof credit.

The anchor audit found checked pinned mathlib mean-value and Poisson formulas but no Harnack
declaration. It also inspected `scottnarmstrong/DeGiorgi` at immutable revision
`4c1b3077d3782b24065184df4ba59501b2e56fc7`: its placeholder-free divergence-form Harnack theorem
is adjacent rather than an exact candidate for this `HarmonicOnNhd` compact-subset target. The
root therefore remains `M3`; see `anchor-audit.json` and `anchor-audit-validation.md`.

The obligation-tree phase freezes an 11-node v1 denominator and separate proof,
refinement, provenance, evidence, trust, documentation, and workflow graphs. The
architecture exposes the local-ball estimate, compact interior cover,
connected-domain ball chain, finite propagation, and uniform-constant assembly
as open obligations. `ObligationTree.lean` checks only the final conversion from
a symmetric uniform value comparison to the exact ratio target. This does not
close the uniform comparison premise or the root.
