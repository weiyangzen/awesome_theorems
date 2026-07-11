# THM-M-0576 rev-5.6 intake

This is the rev-5.6 `planned` dossier for the Atiyah-Bott fixed point theorem for
elliptic complexes. The title is a theorem family, not one syntax-free formula: the
isolated-fixed-point formula and the fixed-submanifold formula have materially
different hypotheses and local terms. The statement phase must select and pinpoint
one primary-source version rather than broaden the theorem by conflating them.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Equivariant Lefschetz/index value equals the sum of Atiyah-Bott local fixed-set terms | The exact source theorem number, coefficient theory, and Lean expression remain open |
| Geometric data | Compact smooth manifold, smooth symmetry, fixed locus, tangent/normal restriction | Concrete mathlib structures and clean/nondegenerate hypotheses are not frozen |
| Analytic data | Equivariant elliptic complex or operator, symbol class, induced cohomology action | No concrete Lean elliptic-operator/index API is credited |
| Local term | Lifted bundle/symbol trace divided by the normal determinant, or its fixed-component analogue | Denominator, orientation, integration, and localization conventions require exact source alignment |
| Boundary cases | Isolated points, positive-dimensional fixed components, empty fixed locus, identity action | No case is excluded merely to simplify the target |
| Existing Lean | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_108.lean` | Legacy abstract data and special-case anchors are discovery inputs, not the classical theorem |
| Trust | Lean 4 kernel plus a pinned mathlib and accepted analytic foundation profile | Toolchain, dependency, axiom, and computation profiles remain open |

The initial proof architecture is: define the equivariant elliptic object and its
Lefschetz number; model the fixed components and normal action; define and justify
the local term; prove the localization/index bridge; compose the component sum.
This is an intake map only, not a frozen obligation registry.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: there is no selected
source-version certificate, normalized kernel expression, environment fingerprint,
checked transport, or mutation suite. The theorem is not complete.

## Validation

The exact commands and results are recorded in `validation.md`. They validate
manifest membership, repository-standard consistency, dossier JSON, and local
reference integrity only.
