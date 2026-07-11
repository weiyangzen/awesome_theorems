# THM-M-1014 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the continuous mapping theorem. The historical
source label is discovery metadata only and supplies no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Weak convergence of probability measures is preserved by pushforward along an everywhere-continuous map | Lean binders, typeclasses, and expression fingerprint belong to the statement phase |
| Measure formulation | `mu_n => mu` implies `map f (mu_n n) => map f mu` | Required Borel/measurability assumptions must be minimized by elaboration, not guessed here |
| Random-variable formulation | Convergence in distribution is preserved by continuous postcomposition | Candidate checked transport only; it is not a second root |
| Stronger mapping theorem | Continuity only outside a `mu`-null discontinuity set | Excluded as a strict generalization of this target |
| Boundary probes | Constant maps, identity maps, Dirac laws, empty/degenerate carrier behavior | Mutation tests and exact typeclass feasibility remain open |
| Foundations | Lean 4 kernel and pinned mathlib under an accepted classical/choice/quotient policy | Toolchain, imports, axioms, and dependency fingerprint remain open |

The initial proof-package surfaces are statement normalization, weak-convergence object-model audit,
pushforward/test-function bridge, topology/measurability side conditions, and a repo-local proof or
pinned wrapper. These are planning surfaces, not a frozen obligation registry.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: there is no elaborated declaration, normalized expression hash,
environment fingerprint, checked transport, or mutation record. The theorem is not complete.

## Validation

The commands and exact intake-level results are recorded in `validation.md`. They validate target
membership, repository-standard consistency, JSON syntax, and dossier hygiene only; no kernel proof
is introduced or claimed.
