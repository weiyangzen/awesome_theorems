# Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root | Brezis-Lieb asymptotic splitting of `p`-power integrals for every real `p > 0` | Exact Lean encoding is open |
| Measure domain | General measure space, following the original theorem family | No finite-measure assumption may be silently added |
| Values | Scalar absolute value/norm, initially real or complex | Scalar generality must be chosen and checked later |
| Convergence | Pointwise almost everywhere | Weak convergence alone is not the root hypothesis |
| Bound | Uniform boundedness of `integral |f_n|^p` | A stronger domination hypothesis would substitute a different theorem |
| Conclusion | Difference of the two sequence integrals converges to the limit integral | Norm convergence, pointwise identities, and finite-sequence claims are excluded |
| Exponent | All finite `p > 0`, including `0 < p < 1` | Restricting to normed `L^p` with `p >= 1` is only a corollary |

The later statement phase must resolve measurability conventions, `integral`
versus `lintegral`, extended-real coercions, and whether the limit's
measurability/integrability is derived or explicit. These are encoding choices,
not permission to broaden or weaken the human theorem.

