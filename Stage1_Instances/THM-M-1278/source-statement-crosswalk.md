# Source-statement crosswalk

## Primary-source candidate

E. Onofri, "On the positivity of the effective action in a theory of random surfaces,"
*Communications in Mathematical Physics* 86 (1982), 321-326, is the historical primary-source
candidate. The bibliographic anchor is intake discovery only: an exact theorem/equation page,
edition image, assumptions, normalization, and errata have not yet been independently inspected,
so this is not `H0` evidence.

## Crosswalk

| Repository phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "Onofri inequality" | sharp logarithmic exponential inequality | exact ordered inequality over integrals | included; elaboration open |
| "on the sphere" | standard round unit `S^2` | concrete Riemannian sphere and volume | included; API open |
| normalized exponential integral | `(4*pi)^-1 integral exp(u)` | measurable exponential and finite integral | included; hypotheses open |
| spherical mean | `(4*pi)^-1 integral u` | real integral against volume | included; normalization open |
| Dirichlet energy | `integral |grad u|^2` | differential/weak gradient and norm square | included; encoding open |
| sharp coefficient | `1/(16*pi)` in this normalization | real constants and checked normalization transports | included; source check open |

## Formalization boundary

No repository-local Lean declaration has been accepted or inspected as an exact anchor during this
intake. The later anchor audit must search the pinned mathlib revision and credible Lean 4 projects,
record exact declaration types and terminal provenance, and must not credit a wrapper whose premise
already contains the inequality.

Before `H0`, a reviewer must verify the primary scan, exact location and wording, definitions,
regularity, measure/metric normalization, equality or sharpness clauses, and errata, then approve a
row-by-row source-to-Lean mapping.
