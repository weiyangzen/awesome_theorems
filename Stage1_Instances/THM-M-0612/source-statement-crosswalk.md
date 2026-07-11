# Source-statement crosswalk

## Candidate primary source

Mikhail Gromov, "Pseudo holomorphic curves in symplectic manifolds," *Inventiones
Mathematicae* 82 (1985), 307-347, is the historical primary-source candidate. The exact numbered
result, page, wording, definitions imported by that result, and relevant errata have not yet been
verified from a stable scan. This bibliographic identification is discovery evidence, not `H0`.

The statement phase must inspect the source itself and may use a modern textbook only as a
secondary interpretation aid. It must not silently infer the exact claim from the conventional
name "nonsqueezing."

## Crosswalk

| Repository/source phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "symplectic nonsqueezing" | sharp obstruction to a ball entering a thinner cylinder | quantified implication or negated embedding | included; exact source anchor open |
| standard ball | open ball in `R^(2n)` of radius `r` | normed coordinate space and open set | included; encoding open |
| symplectic cylinder | `B^2(R) x R^(2n-2)` | distinguished conjugate coordinate plane | included; normalization open |
| symplectic embedding | smooth embedding pulling back the standard two-form | local map, embedding properties, derivative pullback equality | included; API open |
| `r <= R` | sharp capacity/radius conclusion | ordered-real conclusion with positivity hypotheses | included; source formulation open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_256.lean` is discovery input only. It defines a
global self-map datum, coordinate ball and cylinder, a repo-local Gromov-width API, and an unproved
`StatementShape`. A global map on all phase space is potentially narrower than an embedding whose
domain is only the ball, so no exact-statement credit is inherited. Its audit date and mathlib pin
also require fresh verification in the later anchor-audit phase. Reflexive unfolding lemmas and
the checked supporting definitions do not prove nonsqueezing.

Before `H0`, an independent reviewer must approve the primary edition/result/page, every hypothesis
and convention, errata status, and a row-by-row source-to-Lean mapping.
