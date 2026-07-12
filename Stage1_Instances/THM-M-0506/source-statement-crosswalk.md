# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the title `陶伯型定理`, attributes it to Alfred Tauber,
dates it to 1897, and states only `级数收敛与可和性的关系` ("the relationship between series
convergence and summability"). Stage0 repeats this text and explicitly leaves exact definitions,
premises, proof route, equivalent formulations, axioms, and artifacts open. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`.

Thus the repository supplies no edition, paper title, theorem or page, formula, ordered binders,
hypotheses, conclusion, errata record, or formal artifact. The attribution and date are useful
locators, but they do not by themselves distinguish the original theorem from later results bearing
the family name.

## Candidate source work

The 1897 attribution makes Alfred Tauber's original publication the first source candidate for the
statement audit. Intake does not claim a bibliographic edition or quote a formula that has not been
independently inspected. The source phase must obtain an immutable scan or authoritative edition,
pin the exact theorem/page and notation, translate every premise and conclusion, inspect errata,
and have the crosswalk independently reviewed. Modern sources may clarify notation but cannot
silently replace the historical claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "series" | coefficient sequence and its ordinary partial sums | `ℕ -> ℝ` or `ℕ -> ℂ`, `Finset.range`, `HasSum` | APIs probed; domain open |
| "summability" | Abel summability, Cesaro summability, or another method | power-series `tsum` and a specified filter, or a different transform | method absent |
| "relationship" | Tauberian converse from generalized sum to ordinary sum | exact implication plus all side conditions | conclusion absent |
| Alfred Tauber, 1897 | likely locator for the original result | no declaration follows from attribution alone | candidate source locator only |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.Analysis.Complex.AbelLimit`. It checks the generic series predicate,
partial-sum convergence, `tsum`, and the real and complex Abel limit declarations. Mathlib's Abel
limit theorem is the opposite, Abelian direction and is explicitly not crosswalked to the target.
No exact Tauberian converse is credited or claimed by this intake; locating candidates exhaustively
belongs to the later immutable anchor audit after statement freeze.
