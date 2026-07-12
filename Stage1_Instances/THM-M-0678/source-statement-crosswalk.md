# Source-statement crosswalk

## Discovery sources

- Boris Zilber's 1980s work on strongly minimal and categorical structures is the historical source
  family suggested by the metadata attribution and date. No immutable edition or exact numbered
  result has been selected or inspected for this intake.
- John T. Baldwin and Alistair H. Lachlan, "On strongly minimal sets", *Journal of Symbolic Logic*
  **36** (1971), 79-96, is a candidate primary source for the categoricity/strong-minimality branch.
  Its exact theorem wording, incorporated definitions, and corrections remain to be inspected.
- Ehud Hrushovski, "A new strongly minimal set", *Annals of Pure and Applied Logic* **62** (1993),
  147-166, is a candidate primary boundary source because new strongly minimal structures refute
  an unrestricted inference of Zilber's proposed trichotomy. Exact source-to-claim mapping and
  errata review remain open.

These are discovery anchors, not `H0` evidence. Bibliographic identification does not decide which
theorem `THM-M-0678` denotes, and none of these sources has been independently reviewed here.

## Metadata-to-statement crosswalk

| Metadata phrase | Possible source component | Required Lean component | Intake disposition |
|---|---|---|---|
| "strongly minimal theories" | complete theories or definable strongly minimal sets | first-order syntax/semantics, definability with parameters, finite-or-cofinite predicate | domain and convention open |
| "classification" | model spectrum/dimension, geometry, or trichotomy | exact alternatives and exhaustive conclusion | ambiguous; no root frozen |
| Boris Zilber / 1984 | likely points toward geometric classification or trichotomy work | bibliographic provenance only | discovery clue, no proof credit |
| `已验证` | Stage0 screening label | none | rejected as source or machine evidence |
| adjacent Zilber conjecture entry | warns that the same gloss is reused for another target | target-separation constraint | must not merge `THM-M-0679` |

## Required source decision

Before statement acceptance, an accountable reviewer must preserve an immutable primary edition,
identify an exact theorem/page (and incorporated definitions), inspect corrections and later
counterexample literature, and state why that theorem belongs to this target rather than
`THM-M-0679`. The review must enumerate the language and model cardinalities, parameter convention,
strong-minimality domain, categoricity or geometry hypotheses, every classification alternative,
quantifier order, and all exceptional cases.

Only then may a Lean crosswalk map each source object and assumption to concrete declarations and
record missing model-theory APIs. No theorem-specific Lean declaration or formal candidate is
credited at intake; a pinned mathlib/external search belongs to the later anchor-audit phase.

