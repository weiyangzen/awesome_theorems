# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `Frege系统的下界`, attributes it
to Alexander Razborov, gives the year 1985, and repeats only `Frege证明系统的下界` ("lower
bounds for Frege proof systems"). Stage0 marks the precise definitions, assumptions, proof route,
dependencies, axioms, and formal artifacts as `待补充`. The rev-5.6 manifest retains `已验证`
only as `source_status_untrusted`.

This metadata is not a citation and does not determine a proposition. In particular, it does not
say whether "Frege" is unrestricted or bounded-depth, name a hard tautology family, define proof
size, or state a bound. The attribution and year require source verification: they cannot by
themselves distinguish a Frege lower bound from nearby circuit-complexity results.

## Candidate source work

The source audit must first determine whether the catalog intended an unrestricted system, a
bounded-depth system, or another restriction. It must preserve and inspect an immutable primary or
authoritative source, record the exact edition, theorem/page, formal proof-system definition,
formula family, measure, bound, assumptions, errata, and proof boundary, and obtain independent
review. Survey terminology may locate candidates but cannot establish `H0` without this mapping.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Frege system" | exact syntax, axioms/rules, semantics, and presentation equivalence | formula/proof types, checker relation, soundness and completeness | absent |
| "proof" | derivation representation and valid-final-line condition | encoded derivation and decidable or relational verifier | absent |
| "lower bound" | exact rate and ordered asymptotic quantifiers | inequality or asymptotic relation with all binders | absent |
| implicit hard inputs | named tautology family and input parameter | encoded `Nat`-indexed family plus tautology predicate | absent |
| Razborov / 1985 | historical locator | no Lean proposition | unverified metadata, not H evidence |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Computability.Encoding` and `Mathlib.Analysis.Asymptotics.Defs`. It checks
generic encodings, injectivity, list length, eventual filters, and `IsBigO`. These are possible
substrate only. A bounded name search found no mathlib Frege/proof-complexity API or theorem; this
negative name search is not a replacement for the later immutable anchor audit.
