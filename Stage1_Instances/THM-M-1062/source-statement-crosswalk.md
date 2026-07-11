# Source-statement crosswalk

## Primary source candidate

Mark I. Freidlin and Alexander D. Wentzell, *Random Perturbations of Dynamical Systems*, Springer,
is the primary monograph candidate. The repository associates the entry with 1984, consistent with
the first English edition, but no edition, theorem number, page, or errata evidence is present in
the repository. Those details must be inspected and recorded before the statement can reach H0.

This bibliographic identification is a discovery anchor only. No source theorem has been quoted or
credited as verified in this intake.

## Crosswalk

| Repository/source phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Freidlin-Wentzell theory" | family of small-noise asymptotic theorems | one explicitly selected theorem | ambiguous; selection open |
| "randomly perturbed dynamical systems" | small-noise diffusion around an ODE | SDE law indexed by positive noise | intended family only |
| sample-path asymptotics | LDP on a path space | measurable/topological path space and probability laws | candidate, source anchor open |
| action functional | cost of controlled trajectories | extended-real good rate function | candidate, conventions open |
| exponential bounds | lower/upper LDP inequalities | open-set lower and closed-set upper bounds at fixed speed | candidate, normalization open |

## Source-to-formal checks still required

The statement phase must record stable edition metadata and a verbatim theorem anchor, then map every
source quantifier and hypothesis to ordered Lean binders. It must separately identify definitions
incorporated by reference, check errata, and test boundary cases such as zero time, zero noise limit,
inadmissible paths, singular diffusion, and varying initial points. Until then, the Stage0 label
`已验证` is untrusted metadata and provides neither human-source nor machine-proof credit.

No repo-local Lean module or external formal declaration for this target was found by the intake
search. A systematic mathlib/external search belongs to `S56-M-1062-ANCHOR_AUDIT`, after an exact
statement is elaborated.
