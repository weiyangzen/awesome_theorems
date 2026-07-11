# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` says only “distance function's Laplacian,” attributes the result
to many mathematicians in the twentieth century, and labels it verified. This metadata identifies
the theorem family but is neither a mathematical statement nor evidence for `H0` or machine closure.

## Candidate sources requiring inspection

- Eugenio Calabi, “An extension of E. Hopf's maximum principle with an application to Riemannian
  geometry,” *Duke Mathematical Journal* 25 (1958), 45-56. This is a historical source candidate
  for the barrier treatment around the cut locus; exact proposition, wording, and applicability
  have not yet been inspected.
- Jeff Cheeger and David G. Ebin, *Comparison Theorems in Riemannian Geometry*, North-Holland
  Mathematical Library 9 (1975). This is a classical comparison reference candidate; exact
  theorem/page, conventions, and errata remain open.

These are discovery anchors only. The statement phase must inspect a stable copy and choose a
canonical source theorem; an independent source review is required before `H0`.

## Crosswalk

| Repository/source concept | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| distance function | `r(x) = dist(p,x)` | Riemannian distance and smoothness domain | included; encoding open |
| Ricci lower bound | trace curvature bound relative to metric | quantified bilinear/quadratic-form inequality | included; normalization open |
| Laplacian | metric trace of Hessian with fixed sign | Laplace-Beltrami operator on `r` | included; API/sign open |
| model comparison | radial coefficient in constant curvature | explicit model function with domain conditions | included; formula open |
| cut locus | nonsmooth exceptional set | pointwise regular-locus theorem and sourced weak extension | included; semantics open |

No repo-local Lean declaration for this theorem was found during intake. A later immutable-revision
anchor audit must search mathlib and external Lean projects and distinguish neighboring differential
geometry APIs from an exact terminal theorem.

