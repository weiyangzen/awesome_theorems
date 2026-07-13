# Source-statement crosswalk

## Repository records

`Docs/researches/math_theorems.md:5521-5526` supplies the name, Friedberg/Muchnik attribution, year
1956, and gloss `Post problem's affirmative solution`. The six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They give no definitions, binders, assumptions,
proof boundary, bibliography, correction history, or formal artifact.

`Docs/researches/cs_theorems.md:43` independently supplies the more precise gloss `there exist
incomparable recursively enumerable degrees`, with dates 1956-57. Its Stage0 projection is a
separate out-of-scope computer-science UID, `THM-C-0016`; it clarifies the family but transfers no
Stage1 status or proof credit. Stage0 leaves exact premises, proof route, axioms, and machine state
open. The manifest retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Source leads

Walter Dean and Alberto Naibo, *Recursive Functions*, Stanford Encyclopedia of Philosophy,
archived Summer 2026 edition (substantive revision 2024-03-01), Section 3.2, Question 3.1 and
Theorem 3.8, states that there are c.e. sets `A` and `B` with neither Turing reducible to the other.
It explicitly derives intermediate c.e. degrees and attributes the result independently to Muchnik
(1956) and Friedberg (1957). This is a versioned, pinpoint secondary source, not `H0` evidence.

Friedberg's primary article is identified as Richard M. Friedberg, *Two Recursively Enumerable
Sets of Incomparable Degrees of Unsolvability (Solution of Post's Problem, 1944)*, *Proceedings of
the National Academy of Sciences* 43(2) (1957), 236-238, DOI `10.1073/pnas.43.2.236`. Crossref and
Europe PMC metadata confirm this title and locator. The full proof text was access-blocked in this
worker environment and was not accepted.

The secondary source identifies Muchnik's independent publication as A. A. Muchnik, *On the
Unsolvability of the Problem of Reducibility in the Theory of Algorithms*, *Doklady Akademii Nauk
SSSR* 108 (1956), 194-197. Modern Crossref metadata for a Muchnik reprint repeats this bibliography.
No immutable original or reviewed translation was inspected.

## Component crosswalk

| Repository/source component | Prospective mathematical meaning | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| affirmative solution to Post's problem | a nonzero incomplete c.e. Turing degree exists | no canonical degree-of-c.e.-set encoding selected | consequence family identified; exact root relationship open |
| two c.e. sets `A`, `B` | both witnesses are computably enumerable | `REPred A`, `REPred B` for predicates | API elaborates; source and encoding transport open |
| `A` not Turing reducible to `B` | no oracle computation from `B` decides/enumerates the selected representation of `A` | `Not (TuringReducible (oracleOf A) (oracleOf B))` prospectively | `oracleOf` is not selected or defined canonically |
| reverse nonreducibility | the same condition with witnesses exchanged | second `Not TuringReducible` conjunct | binder scope and exact encoding open |
| incomparable c.e. degrees | quotient degrees are unordered in both directions | `TuringDegree` and its partial order | quotient infrastructure exists; c.e.-representative bridge open |
| priority method | finite-injury construction meeting paired requirements | no pinned root declaration located | proof architecture lead, not root evidence |
| `已验证` / `可验证` | catalog labels | no proposition or proof object | no H or M credit |

## Lean and source boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Computability.Halting` provides `REPred`; `Mathlib.Computability.RecursiveIn` provides
oracle recursion; and `Mathlib.Computability.TuringDegree` provides `TuringReducible`,
`TuringEquivalent`, and `TuringDegree` for partial functions. The probe confirms those exact APIs.
A bounded declaration/text search found no Friedberg-Muchnik, Post-problem, or c.e.-degree
incomparability theorem in pinned mathlib or repo-local Lean. This is intake discovery, not an
exhaustive anchor audit or global absence claim.

Before leaving `H1`, reviewers must preserve and hash the primary editions, map every incorporated
definition, premise, construction invariant, and conclusion, audit translations and errata, and
approve the crosswalk. Only then may the statement phase freeze a canonical Lean expression,
compile representation and degree transports, and run semantic mutations.
