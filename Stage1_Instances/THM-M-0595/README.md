# THM-M-0595 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Whitney approximation theorem. The
repository source says only that continuous functions can be approximated by smooth functions.
That wording does not determine the domain and codomain, the approximation topology, the error
quantifier, or whether the intended result is absolute, relative, or map-valued. Intake preserves
that ambiguity rather than silently replacing it with a convenient theorem.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Source claim | Smooth approximation of continuous functions in the Whitney theorem family | The one-line source record does not identify a single exact proposition |
| Domain | A finite-dimensional smooth manifold, with hypotheses sufficient for the selected smoothing argument | Dimension, boundary, countability, paracompactness, and model-space assumptions remain open |
| Codomain | Real/scalar functions as the narrowest candidate; smooth-manifold-valued maps as a distinct standard form | Scalar and map-valued statements are not treated as definitionally identical |
| Approximation | A tolerance-controlled or function-space-topology notion of closeness | Uniform, compact-open, strong/Whitney, and pointwise positive-tolerance forms must not be conflated |
| Relative form | Preservation where the original map is already smooth, possibly near a closed subset | This is a strengthening and is not part of the root without a source decision |
| Homotopy form | Smooth approximation of a map together with a homotopy from the original map | Homotopy is a candidate consequence/formulation, not intake proof credit |
| Proof architecture | Chartwise smoothing, locally finite refinement, partition-of-unity assembly, error control, and target-range control | Scope nodes only; no obligation registry or closure is frozen |
| Foundations | Lean 4 kernel plus pinned mathlib and an audited manifold/partition-of-unity profile | Imports, versions, axioms, TCB, and environment fingerprint remain open |

The provisional architecture is local smoothing -> locally finite assembly -> approximation-error
control, followed by range control and homotopy for a manifold-valued form, and relative
preservation if that stronger form is selected. These are scope-map nodes, not accepted proof
obligations or proof coverage.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H1, M4, R3]`. The first open theorem gate
is exact-statement identity. A classical theorem family and primary historical source are known,
but the repository wording is too weak to choose among inequivalent standard formulations. The
dependent statement phase must pin a precise source theorem and freeze every binder, hypothesis,
topology, tolerance, and boundary case before elaboration. The theorem is not complete.

## Validation

The smallest real intake checks and exact outcomes are recorded in `validation.md`. They validate
manifest membership, repository-standard consistency, JSON syntax, required dossier files, and
local hygiene only. No Lean declaration is introduced, so no kernel result is claimed. Master
acceptance and all dependent phases remain outstanding.
