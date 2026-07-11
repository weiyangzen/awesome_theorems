# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Sharp first-order Sobolev inequality on Euclidean `R^n`, `1 < p < n` | Exact Lean expression and explicit constant are open |
| Test class | Real-valued compactly supported smooth functions | Completion to a homogeneous Sobolev space needs a checked density transport |
| Norms | Lebesgue `L^p` gradient norm and `L^(np/(n-p))` function norm | Bochner/scalar and `ENNReal`/`Real` conventions are not selected |
| Sharpness | The displayed constant is the least admissible constant | Extremizer construction and equality classification are separate obligations |
| Geometry | Standard Euclidean measure, norm, and weak/classical gradient agreement on smooth functions | Manifolds, bounded domains, weights, and anisotropic variants are excluded |
| Foundations | Lean 4 and pinned mathlib analysis stack | Imports, toolchain pin, axioms, and TCB closure are open |

## Exclusions

This target does not denote Talenti's elliptic rearrangement comparison theorem,
the Aubin-Talenti extremizer classification as a standalone theorem, fractional
Sobolev inequalities, endpoint `p = 1`, the critical case `p = n`, or embeddings
on general domains/manifolds. Similar names do not license substituting one of
those claims for this root.

## Planned statement decisions

The dependent statement phase must select the explicit gamma/volume formula for
`C_Talenti(n,p)`, prove its equivalence to the primary source convention, choose
the function-space and integration encodings, elaborate the exact target, and
mutation-test `1 < p`, `p < n`, compact support, gradient, sharpness, and the zero
function boundary. None of these checks is credited by this intake.
