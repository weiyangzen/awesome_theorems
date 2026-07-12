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
| standard ball | open ball in `R^(2n)` of radius `r` | `ball r`, using the coordinate norm and `< r^2` | elaborated; source approval open |
| symplectic cylinder | `B^2(R) x R^(2n-2)` | `cylinder i R`, bounding one conjugate pair | elaborated; source approval open |
| symplectic embedding | smooth embedding pulling back the standard two-form | `IsSymplecticEmbeddingOnBall`, with all conditions restricted to the ball | elaborated; source approval open |
| `r <= R` | sharp capacity/radius conclusion | positive radii and conclusion `r <= R` | elaborated; source approval open |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_256.lean` is discovery input only. It defines a
global self-map datum, coordinate ball and cylinder, a repo-local Gromov-width API, and an unproved
`StatementShape`. A global map on all phase space is potentially narrower than an embedding whose
domain is only the ball, so no exact-statement credit is inherited. Its audit date and mathlib pin
also require fresh verification in the later anchor-audit phase. Reflexive unfolding lemmas and
the checked supporting definitions do not prove nonsqueezing.

The worker-proposed canonical target is `Stage1.THM_M_0612.StatementShape` in `Statement.lean`.
Before `H0`, an independent reviewer must approve the primary edition/result/page, every hypothesis
and convention, errata status, and this row-by-row source-to-Lean mapping.

The 2026-07-12 anchor audit also found `hrmacbeth/symplectic` declaration
`gromovNonsqueezing` at immutable commit
`acc509702046aaae6a3c9be4546d5735ad7450cf`. Its theorem body is `sorry`, as are
11 supporting definitions/proofs in the same four-file project. Its capacity-normalized parameters
and manifold-map interface are therefore useful comparison material only, not source fidelity or
machine-proof evidence. See `anchor-audit.md` for the complete candidate inventory.
