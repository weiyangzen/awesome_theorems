# Anchor audit

The frozen target is `Stage1Instances.THM_M_1177.AlexandrovBakelmanPucciTarget`, expression SHA-256
`bb3ff2384920048fe79eb0bad3c47a32db31bdaf4e4595898cbd5c7dbfb6ac41`. The dependency closure uses
Lean `v4.29.0` and mathlib commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Verdict

No declaration with the exact ABP statement was found in pinned mathlib, the repository-local Lean
sources, or the external Lean 4 projects listed in `anchor-audit.json`. The exact root therefore
remains `M4`. The checked mathlib declarations are component anchors only and receive no root proof
credit. In particular, the Jacobian theorems assume injectivity, while the ABP gradient-map step
needs additional contact-set geometry and multiplicity/decomposition work.

The external search is fail-closed. Immutable repository trees were inspected where available, but
anonymous GitHub code search required authentication and grep.app returned an HTTP 429 challenge.
Those limitations are evidence gaps, not negative proof that an implementation exists nowhere.

## Candidate boundary

| Surface | Pinned declaration | Assessment |
|---|---|---|
| Change of variables | `MeasureTheory.lintegral_abs_det_fderiv_eq_addHaar_image` and its integral variants | Credible area-formula ingredients; statement mismatch |
| AM-GM | `Real.geom_mean_le_arith_mean` | Scalar algebraic ingredient; missing matrix bridge |
| Positive definiteness | `Matrix.posDef_iff_dotProduct_mulVec`, `Matrix.PosDef.det_pos` | Useful encoding and determinant positivity; no PDE conclusion |
| Convex maximum principle | `ConvexOn.exists_ge_of_mem_convexHull` | Related convexity lemma; no upper-contact-set or normal-map theorem |

Exact structured details, external revisions, query limitations, and classifications are in
`anchor-audit.json`. `AnchorAudit.lean` checks that each pinned component declaration elaborates and
prints axiom dependencies for representative anchors. This node supplies no theorem proof.

## Validation

Exact commands and results are recorded in `anchor-audit-validation.md`. Master acceptance remains
required before the dependent obligation-tree phase may claim this node.
