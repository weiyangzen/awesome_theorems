# Source-statement crosswalk

## Authoritative repository record

`Docs/researches/math_theorems.md:10041-10046` supplies exactly the title
`Euler-Lagrange方程`, attribution `Leonhard Euler/Joseph Lagrange`, year 1755, the gloss
`泛函极值的微分方程` (a differential equation for extrema of functionals), high importance, and
status `已验证`. Git history places all six lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula, domain,
definition, binder, regularity or boundary hypothesis, conclusion, proof boundary, erratum, or
formal artifact.

`Docs/Stage0_Blueprint.md:37479-37504` repeats the gloss while leaving the target formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Component crosswalk

| Catalog component | Candidate mathematical readings | Required formal surface | Intake assessment |
|---|---|---|---|
| "functional extrema" | local minimum, local maximum, local extremum, or stationary first variation | exact extremum/stationarity predicate and admissible variation space | open; these premises are not interchangeable without hypotheses |
| "functional" | one-dimensional integral, multiple-integral functional, abstract functional, or mechanical action | exact domain, codomain, integrand, measure/integral, and derivative definitions | open |
| "differential equation" | classical Euler-Lagrange ODE, coordinate system, weak equation, PDE analogue, or variational-gradient identity | exact conclusion, equality convention, regularity, and locus | open |
| Euler/Lagrange and 1755 | historical attribution only | immutable source edition and pinpoint with assumption/errata mapping | no cited source and no H0 credit |
| `已验证` | source inventory label | no proposition or proof object | no H or M credit |

## Contextual repository records

The separate physics record `Docs/researches/physics_theorems.md:6386-6392` says that the
Euler-Lagrange equation is a necessary condition for extrema and writes `delta integral L dt = 0`.
It belongs to `THM-P-0749`, gives no Euler-Lagrange differential formula or full assumptions, and
cannot amend this target's source record.

`THM-M-1377` names the broader calculus of variations, while `THM-M-1382` and `THM-M-1518` name
least action. The last target's dossier cites Hamilton and Lanczos as discovery leads and later
chooses fixed-endpoint stationary action implying an interior equation. Those choices belong to a
different target and are not admitted here as provenance or an alternate encoding.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, adjacent APIs include
`IsLocalMin.fderiv_eq_zero`, `IsLocalMax.fderiv_eq_zero`, `IsLocalExtr.fderiv_eq_zero`,
`intervalIntegral.integral_deriv_smul_eq_sub_of_hasDeriv_right`,
`intervalIntegral.integral_smul_deriv_eq_deriv_smul_of_hasDerivAt`, and line-derivative
integration-by-parts results. A bounded exact-topic search found no terminal Euler-Lagrange theorem
in pinned mathlib. This is intake discovery, not the exhaustive immutable anchor audit.

The legacy `S1_M_186.lean` abstractly assumes the decisive bridge;
`S1_M_187.lean` defines a concrete-looking equation but its main statement shape has the converse
direction; `S1_M_184.lean` proves only the zero-Lagrangian real-line equation for every path, with
no extremum-to-equation implication. The distinct
`THM-M-1518` statement module also supplies no source-approved transport to this unresolved target.
None receives proof credit.

Before leaving `H5`, an accountable source reviewer must select one immutable proposition, map all
incorporated definitions, ordered binders, hypotheses, conclusion, proof boundary, and errata, and
obtain independent approval. Only then may the statement phase choose minimal pinned imports,
elaborate and fingerprint the exact target, compile checked transports, and run removed-hypothesis,
changed-domain, binder-scope, and boundary mutations.
