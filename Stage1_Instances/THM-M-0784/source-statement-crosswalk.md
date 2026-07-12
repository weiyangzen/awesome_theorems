# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `适当力迫公理`, attributes it to
Saharon Shelah, dates it to 1982, and gives only `PFA及其推论` ("PFA and its consequences"). Stage0
repeats that metadata without definitions or a proof source. The rev-5.6 manifest preserves
`已验证` solely as `source_status_untrusted`. No formula, named consequence, base theory, theorem,
edition, page, errata record, or formal artifact is supplied.

## Candidate source work

James E. Baumgartner's chapter *Applications of the Proper Forcing Axiom* in the *Handbook of
Set-Theoretic Topology* (1984) and Saharon Shelah's *Proper and Improper Forcing* are candidate
locators for definitions, consistency results, and consequences. No edition or exact passage has
been accepted during intake. The source audit must inspect an immutable edition, identify whether
the intended target is the axiom, a relative-consistency statement, or one named consequence, and
record its precise definition/theorem/page, base theory, assumptions, proof boundary, and errata.
Until independent review, these references are discovery leads rather than `H0` evidence.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| PFA | quantification over proper forcing notions | internal forcing notion and properness predicate | absent; generic `PartialOrder` only probed |
| dense sets | a family of dense subsets of a forcing order | chosen order orientation and `Dense` predicate | generic API probed; semantics open |
| `aleph_1` bound | at most `aleph_1` many dense sets, or an `omega_1` index | `Cardinal.aleph`/cardinality bound | cardinal API probed; convention open |
| meeting filter | filter or directed set meeting each dense set | `Filter` or a checked alternate encoding | generic API probed; encoding open |
| "consequences" | one or many theorems derived assuming PFA | exact hypothesis and named conclusion | no consequence selected |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports order/filter and cardinal modules and checks generic types for `PartialOrder`,
`Filter`, sets/pairwise relations, cardinality, `aleph`, and `aleph_1`. Mathlib has no checked
forcing-density predicate in this probe; it would have to be defined after the order convention is
frozen. These are encoding ingredients only. A bounded name/content search found no mathlib forcing/PFA development under
`Mathlib/SetTheory`; that observation is not a substitute for the later immutable anchor audit.
