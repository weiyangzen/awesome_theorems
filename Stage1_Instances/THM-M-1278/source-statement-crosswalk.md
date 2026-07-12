# Source-statement crosswalk

## Primary-source candidate

E. Onofri, "On the positivity of the effective action in a theory of random surfaces,"
*Communications in Mathematical Physics* 86 (1982), 321-326, is the historical primary-source
candidate (DOI `10.1007/BF01212171`). Its publisher abstract was inspected during the statement
phase. It explicitly specifies `C-infinity` functions on the two-dimensional sphere and the
constraint `integral (exp eta - 1) dmu0 = 0`, under which the displayed action is nonnegative.
The full article, equation pages, area convention, and errata remain unverified, so this is not
`H0` evidence.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Onofri inequality" | sharp logarithmic exponential inequality | `OnofriInequality` | elaborated |
| "on the sphere" | standard round unit `S^2` | `Sphere2 = Metric.sphere 0 1` in `EuclideanSpace Real (Fin 3)` | elaborated |
| normalized exponential integral | `(4*pi)^-1 integral exp(u)` | Bochner integral against `sphereArea` | elaborated |
| spherical mean | `(4*pi)^-1 integral u` | Bochner integral against `sphereArea` | elaborated |
| Dirichlet energy | `integral |grad u|^2` | `dirichletEnergy` using the ambient gradient's tangent projection | elaborated |
| sharp coefficient | `1/(16*pi)` in this normalization | literal real constants; mutation changes it to `1/(8*pi)` | elaborated and distinguished |

## Formalization boundary

The normalized target follows algebraically from the publisher abstract's constrained form by
setting `eta = u - log((1/(4*pi))*integral exp u)`, taking the standard unit-sphere area to be
`4*pi`, and observing that adding a constant does not change the gradient. This statement node
records that crosswalk but does not claim a formally checked transport from the source notation.

No repository-local proof declaration has been accepted as an exact anchor. The later anchor audit
must search the pinned mathlib revision and credible Lean 4 projects,
record exact declaration types and terminal provenance, and must not credit a wrapper whose premise
already contains the inequality.

Before `H0`, a reviewer must verify the primary scan, exact location and wording, definitions,
regularity, measure/metric normalization, equality or sharpness clauses, and errata, then approve a
row-by-row source-to-Lean mapping.
