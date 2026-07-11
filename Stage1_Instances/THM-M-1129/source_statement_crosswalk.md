# Source-statement crosswalk

The Stage0 phrase `二维波动方程的解` identifies a theorem family, not one exact theorem. The
following are discovery anchors. They do not yet satisfy the rev-5.6 immutable-edition, pinpoint,
assumption, errata, and independent-review requirements for `H0`.

| Claim component | Human source anchor | Planned Lean surface | Intake assessment |
|---|---|---|---|
| Two-dimensional wave Cauchy problem and Poisson representation | F. John, *Partial Differential Equations*, 4th ed., Springer, 1982, chapter on the wave equation and method of descent | functions on `EuclideanSpace Real (Fin 2)`, `laplacian`, time derivatives, disk integral | Standard primary textbook anchor located; exact section/page and hypotheses need edition inspection |
| Derivation by descent from Kirchhoff's formula | L. C. Evans, *Partial Differential Equations*, 2nd ed., AMS, 2010, Section 2.4, wave equation, Poisson's formula | a future checked descent/change-of-variables bridge | Secondary textbook anchor; not proof credit |
| Initial displacement term | classical formula `d/dt ((1/(2*pi*c)) integral_(|y-x|<ct) f(y)/sqrt(c^2*t^2-|y-x|^2) dy)` | Bochner/Lebesgue integral plus a time derivative | Constant and regularity must be checked before formal freezing |
| Initial velocity term | classical formula `(1/(2*pi*c)) integral_(|y-x|<ct) g(y)/sqrt(c^2*t^2-|y-x|^2) dy` | same disk integral without outer derivative | Boundary singularity and integrability remain explicit obligations |
| Initial data and uniqueness | limiting recovery at `t=0` and uniqueness among sufficiently regular solutions | limits/derivatives at zero and a wave-energy or representation uniqueness theorem | Precise solution class is unresolved; no uniqueness claim is frozen |

The prospective display is recorded only to disambiguate the name. It is not yet the canonical Lean
target. In particular, compact support versus decay/integrability assumptions, `C^2`/`C^3`
regularity, classical versus weak solution, and whether the theorem asserts construction,
representation of every solution, or both materially change the claim.

Required follow-up: inspect and hash a specific source edition; record exact pages/theorem labels and
errata; map every assumption to the final ordered binders; inspect mathlib's actual PDE, Laplacian,
measure, and change-of-variables APIs at the repository pin; then elaborate and mutation-test the
chosen statement. No `H0` or machine closure is claimed.
