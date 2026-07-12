# Statement-phase blocker

Item: `S56-M-1320-STATEMENT`

## Verdict

The exact Lean target cannot truthfully be frozen or elaborated in the pinned environment. This
phase is blocked, and no canonical theorem declaration or statement-completion receipt is claimed.

There are two independent first-order blockers:

1. The intake correctly requires the exact theorem/corollary, page, hypotheses, sign convention,
   and numerical constant from Li--Yau's primary text. The immutable bibliographic record identifies
   DOI `10.1090/pspum/036/573435`, pages 205--239, but the publisher endpoint rejected automated
   access and OpenAlex reports no open full text. Metadata cannot establish the exact mathematical
   statement. In particular, importing the commonly reported nonnegative-Ricci specialization
   would not establish which dimension, connectedness, boundary, eigenvalue, or Laplacian
   conventions occur in the selected primary result.
2. A source-tree search of pinned mathlib revision
   `8a178386ffc0f5fef0b77738bb5449d50efeea95` found Riemannian manifold and metric-diameter APIs,
   but no Ricci-curvature, Laplace--Beltrami, or first-eigenvalue declaration. The existing
   `Mathlib.Analysis.InnerProductSpace.Laplacian` is a Euclidean inner-product-space Laplacian and
   is not a valid substitute for the geometric operator.

`StatementProbe.lean` therefore checks only the available vocabulary. It is intentionally not a
theorem statement and earns no machine-closure credit. Creating abstract `ricci`, `lambdaOne`, or
diameter parameters would assume away the missing geometric definitions and would broaden the
target, contrary to the rev-5.6 exact-statement gate.

## Environment

- Repository base: `86b5fbdd7aeb66bbca3069f46c207c1d5f20790e`
- Lean toolchain: `leanprover/lean4:v4.29.0`
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- `.lake`: reused canonical artifact via symlink; it was not mutated

## Validation record

Run on 2026-07-12 from the worker clone unless a different working directory is stated.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1320` | exit 0; rank 482, L0/rework_required, planned, theorem_complete false |
| `rg -n -i '\\bRicci\\b\|RicciCurv\|Laplace.Beltrami\|Beltrami\|first.*eigen' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1; no matching pinned declarations |
| `rg -n 'Riemannian\|Ricci\|Laplacian\|Laplace' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 0; Riemannian manifold and Euclidean Laplacian files found; no geometric spectral API found |
| `lake env lean ../../Stage1_Instances/THM-M-1320/StatementProbe.lean` from `Formalizations/Lean` | exit 0; printed types of `IsRiemannianManifold`, `Metric.diam`, and `IsCompact` |

## Retry condition

Retry statement execution only after (a) an inspectable stable copy of the primary theorem fixes the
exact source statement and errata status, and (b) concrete pinned Lean interfaces for Ricci
curvature, the scalar Laplace--Beltrami spectrum/first positive eigenvalue, and the corresponding
Riemannian diameter are available or are implemented as separately validated foundations. Until
then the root remains at least `M4`, and downstream anchor, obligation, proof, validation, and
release phases remain open.
