# THM-M-0416 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Dirichlet's unit theorem. Historical
Stage1 files and the manifest's untrusted source label are discovery inputs only; neither confers
accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Human root | For a number field `K` with `r₁` real places and `r₂` pairs of complex places, `O_K^×` is the product of its finite roots-of-unity subgroup and a free abelian group of rank `r₁ + r₂ - 1` | Exact source theorem/page and convention audit remain open |
| Lean root candidate | The quotient of `(O K)^×` by torsion is finite free over `Z` of mathlib unit rank, together with unique torsion-times-fundamental-units decomposition | Legacy `StatementShape` is unaccepted discovery; elaboration belongs to the statement phase |
| Object model | number field, ring of integers, unit group, torsion subgroup, infinite places, fundamental units | Identification of mathlib `rank K` with `r₁ + r₂ - 1` must be checked explicitly |
| Degenerate cases | `K = Q`, rank zero, empty family of fundamental units, torsion-only units | No boundary mutation has yet been accepted |
| Mathematical architecture | logarithmic embedding, lattice discreteness/cocompactness, rank computation, torsion kernel, decomposition | Architecture only; no proof node is closed by this intake |
| Foundations | Lean 4 kernel plus pinned mathlib; classical choice and quotient constructions | Exact toolchain, dependency closure, TCB, and computation profile remain open |

The structured claim is in `intake.json`; `source_statement_crosswalk.md` maps its components to
human and Lean discovery sources.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The exact-statement gate is the
first failed theorem gate: no accepted elaborated expression hash, environment fingerprint,
transport, or mutation evidence exists. This intake does not claim theorem completion.

## Validation

`validation.md` records membership, standard, syntax, and dossier-integrity checks. These are not
kernel-proof evidence, and master acceptance plus every dependent phase remain outstanding.
