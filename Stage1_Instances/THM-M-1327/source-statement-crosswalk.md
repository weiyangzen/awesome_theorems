# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives only the name "Hessian comparison theorem", the gloss
"Hessian of the distance function", a twentieth-century date, and an untrusted "verified" label.
`Docs/Stage0_Blueprint.md` repeats that metadata and explicitly leaves assumptions and artifacts
open. Neither is a mathematical primary source, and neither fixes an exact proposition.

## Candidate theorem sources

- Jeff Cheeger and David G. Ebin, *Comparison Theorems in Riemannian Geometry*, North-Holland
  Mathematical Library 9 (1975), the distance-function comparison material.
- Peter Petersen, *Riemannian Geometry*, Graduate Texts in Mathematics 171, Springer, comparison
  geometry chapter (edition to be selected).

These are discovery candidates only. No edition-specific theorem number, page, wording, errata, or
proof has been inspected in this intake, so they provide no `H0` credit. The statement phase must
choose a stable edition and transcribe one theorem rather than combine familiar variants.

## Crosswalk

| Repository phrase | Exact component to recover from source | Required Lean component | Intake status |
|---|---|---|---|
| distance function | base point, domain, and `r = dist p` | Riemannian distance and smooth locus | family included; domain open |
| Hessian | convention and evaluation form | Hessian as a symmetric bilinear form | included; API/convention open |
| comparison | inequality direction and equality/model term | order on quadratic forms or pointwise vector inequality | variant open |
| curvature hypothesis | sectional upper or lower bound, local/global quantifiers | sectional curvature predicate along relevant geodesics | sign and scope open |
| model space | constant curvature and Jacobi/model coefficient | explicit model function with singular-radius conditions | parameterization open |

## Non-substitution check

Tracing `Hess r` yields a Laplacian comparison only after dimension and transverse-direction facts;
the trace result cannot be used to reconstruct the stronger bilinear inequality. Conversely, a
Rauch/Jacobi-field theorem is a likely proof dependency, not the source statement itself.

Before `H0`, an independent reviewer must verify edition, theorem/page, definitions, every
assumption, curvature/Hessian sign conventions, exceptional radii, errata, and every row of the
source-to-Lean mapping.
