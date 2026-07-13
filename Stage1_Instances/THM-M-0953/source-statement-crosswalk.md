# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:6959-6964` records the Chinese title `Solymosi定理`, attributes it
to József Solymosi, dates it to 2009, and gives only `和集与积集的下界改进`. The record has no
bibliography, formula, domain, assumptions, constants, parameter regime, proof boundary, or
errata. `Docs/Stage0_Blueprint.md:25984-26009` repeats this metadata and explicitly leaves precise
definitions, premises, proof route, dependencies, alternate statements, axioms, and formal
artifacts open. The manifest preserves `已验证` as `source_status_untrusted`; it supplies no proof
credit.

## Inspected primary-source candidate

József Solymosi, *Bounding multiplicative energy by the sumset*, *Advances in Mathematics* 222(2)
(2009), 402-408, DOI `10.1016/j.aim.2009.04.006`, is an exact author/year/topic match. The immutable
preprint `arXiv:0806.1040v3` was inspected; its PDF SHA-256 is
`a48837d2d5e3bcb2af02593aa6315699347c5440a69d3f495c2c0fe2f0b853f2`.

The paper's page 2 states Theorem 2.1 for a finite set of positive reals and then Corollary 2.2 as
the improved max-form sum-product bound. This is strong discovery evidence, but it is not an `H0`
crosswalk: the catalog does not cite or choose the paper/result, the source has not received
independent review, the log convention and singleton boundary remain unresolved, and no errata
audit or source-to-proof-node mapping is accepted. The arXiv API title, *An upper bound on the
multiplicative energy*, also differs from the v3 PDF/publication title, so the edition relationship
must remain explicit.

## Crosswalk

| Repository phrase | Candidate source component | Required Lean component | Intake status |
|---|---|---|---|
| `Solymosi`, 2009 | sole-author 2009 journal article above | immutable source identity and selected numbered result | strong match, not catalog-authorized |
| "sumset" | `A + A = {a + b | a,b in A}` | pointwise addition of a finite set of reals | substrate elaborates |
| "product set" | `AA = {ab | a,b in A}` | pointwise multiplication of the same finite set | substrate elaborates |
| "lower-bound improvement" | Theorem 2.1 or its Corollary 2.2 | one exact inequality with all casts, powers, max, and constants | candidate family only |
| domain | finite set of positive real numbers in both candidates | `Finset Real` plus elementwise strict positivity, or an approved equivalent | not frozen |
| size | finite cardinality | `Finset.card` with explicit coercions | substrate elaborates |
| logarithmic loss | ceiling of an unspecified printed `log` | approved base, ceiling, codomain, denominator, and small-cardinality policy | unresolved and blocking |
| `已验证` | untrusted catalog inventory field | no proposition or proof evidence | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` imports `Mathlib.Combinatorics.Additive.Energy` and checks pointwise `A + A`,
`A * A`, their cardinalities, `Finset.mulEnergy`, its sum-of-squares identity, the standard
energy/cardinality lower-bound substrate, and `Nat.clog`. The probe also elaborates an explicitly
uncredited candidate `Finset Real → Prop` with base-two `Nat.clog` and a `1 < A.card` guard. A
bounded exact-topic search found the energy API but no `Solymosi` or source-identical sum-product
theorem. These are encoding and search-boundary facts only. They do not select a canonical
proposition, prove Solymosi's upper-energy lemma, or provide machine closure.

## Admission work

To advance, independent source and formal reviewers must admit a lawful immutable edition, select
Theorem 2.1, Corollary 2.2, or another exact result, map every definition and assumption, resolve the
logarithm and small-cardinality issue, record corrections and errata, and authorize the ordered Lean
target. Only then may the statement phase minimize imports, elaborate and hash the expression,
compile checked relationships to alternate forms, and run all required statement mutations.
