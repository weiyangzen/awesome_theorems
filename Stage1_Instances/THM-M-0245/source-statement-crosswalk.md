# Source-statement crosswalk

## Repository record

The repository catalog records:

| Field | Literal value | Intake interpretation |
|---|---|---|
| Title | `法图定理` | Identifies the Fatou theorem family, not one expression. |
| Attribution | Pierre Fatou | Historical metadata; no theorem locator is supplied. |
| Year | 1906 | Consistent with the discovered publication lead, but not a statement fingerprint. |
| Gloss | `单位圆盘内全纯函数的径向极限` | Names disk holomorphic functions and radial limits but omits the size premise, boundary measure, quantifiers, and conclusion. |
| Status | `已验证` | Explicitly untrusted under rev-5.6; yields no H/M/R or proof credit. |

The Stage0 projection repeats this record while leaving the precise definitions and premises,
proof history, dependencies, equivalent formulations, axioms, machine status, and artifact links
open.

## Historical source lead

Crossref metadata identifies P. Fatou, *Series trigonometriques et series de Taylor*, *Acta
Mathematica* 30 (1906), 335-400, DOI `10.1007/BF02418579`. DOI resolution points to Project
Euclid. A zbMATH/JFM record for the same paper describes Poisson-integral boundary behavior and
uses an almost-everywhere convention, which supports the historical family identification.

This remains an `E5` bibliographic and review-record lead. The primary PDF endpoint returned an
access-control HTML page rather than the paper, so no original theorem/page passage, incorporated
definition chain, exact premise, conclusion, proof boundary, translation, correction, or erratum
was inspected. The secondary review text is not substituted for the primary statement and does not
establish H0.

## Missing source-to-claim nodes

| Claim component | Repository evidence | State required before statement freeze |
|---|---|---|
| Function domain | "unit disk" | Fix open disk carrier and every coercion/topology convention. |
| Analytic premise | "holomorphic function" | Fix the exact analytic predicate and its domain. |
| Size premise | absent | Select boundedness, exact Hardy-class membership/exponent, or another source premise. |
| Boundary variable | absent | Fix circle or angle carrier, endpoint quotient, and boundary measure. |
| Approach region | "radial" only | Define the radius domain and one-sided filter; decide whether nontangential convergence is also asserted. |
| Limit | "radial limit" only | Fix existence, finiteness/codomain, boundary function, and any uniqueness or norm conclusion. |
| Exceptional set | absent | Fix the almost-everywhere quantifier and null-set semantics. |
| Degenerate cases | absent | Decide zero/constant functions, exponent endpoints, representatives, and measure normalization. |

The bare gloss cannot be promoted to an unconditional all-holomorphic proposition. A familiar
bounded or Hardy-space version is a candidate only until the primary source and an independent
review select and map it.

## Lean crosswalk

Pinned mathlib exposes `Complex.UnitDisc`, `AnalyticOnNhd`, `circleMap`, one-sided filter
and `Tendsto` machinery, and almost-everywhere/periodic-circle measure APIs. A bounded local search
found no declaration named for Fatou's complex boundary theorem, radial or nontangential boundary
limits, or analytic Hardy spaces. The only broad `Fatou` hits were measure-theoretic Fatou's lemma
references.

`IntakeProbe.lean` re-elaborates ten adjacent interfaces. It deliberately does not define a Hardy
class, choose a boundary measure or limit proposition, or declare a theorem. Therefore:

- canonical Lean module/expression and expression hash: open;
- exact environment fingerprint and minimal imports: open;
- checked alternate transports and statement mutations: open;
- proof-body location and provenance: none credited; and
- source fidelity, audit completion, and theorem completion: false.

## Retry condition

Preserve an immutable primary copy, identify the exact theorem and complete definition chain,
translate every premise and conclusion, audit corrections and errata, and obtain independent source
approval. Only then may the statement phase choose one proposition, elaborate it in the pinned Lean
environment, and test transports and mutations.
