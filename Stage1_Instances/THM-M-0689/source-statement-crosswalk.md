# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `证明复杂性`, attributes it to Stephen
Cook, gives the year 1971, and states only `证明长度的下界` ("lower bounds on proof length"). Stage0
repeats those fields while marking the exact definitions, assumptions, proof process, date, source,
and artifacts as `待补充`. The rev-5.6 manifest preserves `已验证` only in the explicitly untrusted
field `source_status_untrusted`.

This is not a pinpoint source citation and does not determine a proposition. The same source file
separately lists Haken's pigeonhole-principle lower bound and a later generic "proof complexity lower
bounds" entry. Those nearby records demonstrate that multiple lower-bound claims are in scope, but
they do not crosswalk any one of them to `THM-M-0689`.

## Candidate source work

Cook's 1971 work and the later Cook-Reckhow definition of propositional proof systems are candidate
historical locators, not accepted theorem sources in this intake. The anchor/source phases must
inspect immutable editions and determine whether the catalog intended a definition/framework, a
specific lower-bound theorem, or a survey-level field label. A valid H crosswalk must record the
exact theorem/page, proof system, formula family, measure, bound, assumptions, errata, and an
independent review. No such source is inferred here.

## Crosswalk

| Repository phrase | Required mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "proof" | syntax plus a sound proof-checking relation/system | proof/formula types, checker relation, soundness and any completeness condition | absent |
| "length" | a fixed representation and size measure | encodings and a `Nat`-valued size function | generic encoding/length APIs probed; exact measure open |
| "lower bound" | an explicit rate and exact asymptotic quantifiers | inequality or asymptotic relation with ordered binders | absent |
| implicit hard inputs | a named formula family and size parameter | encoded family indexed by `Nat` and truth/unsatisfiability predicate | absent |
| Stephen Cook / 1971 | historical locator | no Lean proposition | unverified metadata, not H evidence |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Computability.Encoding` and `Mathlib.Analysis.Asymptotics.Defs`. It checks
generic encodings, injectivity of encoding, list length, eventual filters, and asymptotic `IsBigO`.
These are only possible ingredients. No proof-system definition, hard formula family, or theorem
corresponding to the repository gloss was found by the bounded repo-local name search; that search
is not a replacement for the later immutable anchor audit.
