# THM-M-1045 obligation tree

The frozen root is `CameronMartinTarget`. Machine eligibility was selected before inspecting
closure. The root remains open: the conditional Lean composition consumes, but does not prove,
the equivalence, density, and singularity packages.

## M1045-root

`M1045-T-ASSEMBLE` composes all three branches. Statement/foundation, normalization, source,
provenance, and documentation edges are separate from proof premises.

## M1045-b-equivalence

The admissible branch requires finite-dimensional cylinder shifts and extension to the path
sigma-algebra. Both absolute-continuity directions are required.

## M1045-b-density

This branch requires an actual Paley-Wiener construction and its law, followed by extension and
Radon-Nikodym identification with the frozen positive-sign exponential.

## M1045-b-singularity

The negative branch requires a Gaussian separation argument for every direction outside the
integral representation. It is not implied by failure of the positive proof.

## Statement-model risk

`WienerData.paleyWienerIntegral` currently carries measurability but no isometry, Gaussian-law, or
compatibility field. Because the exact target quantifies over every `WienerData`, downstream proof
work must derive enough pairing behavior from the remaining fields or demonstrate that the frozen
statement needs a new statement-registry version. This obligation freeze does not silently add a
coherence hypothesis.

## Status boundary

The architecture, denominator, typed edges, and conditional composition are self-tested only.
Human status remains `H1`, machine root status `M3`, and readability `R3`. There is no theorem,
audit, source-review, or release completion claim.
