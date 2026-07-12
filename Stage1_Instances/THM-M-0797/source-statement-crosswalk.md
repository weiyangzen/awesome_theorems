# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records only the title `钻石原理`, attributes it to Ronald
Jensen, gives the year 1972, and states `组合集合论原理` ("combinatorial set-theory principle").
Stage0 repeats that gloss and leaves the exact definition, assumptions, proof route, dependencies,
axioms, and formal artifact open. The rev-5.6 manifest preserves `已验证` solely as
`source_status_untrusted`.

Those records give no formula, cardinal parameter, stationary-set parameter, ambient model,
hypotheses, conclusion, edition, theorem/page, proof source, or errata. In particular they do not
say whether the requested item is the diamond assertion itself or Jensen's relative theorem about
the constructible universe. The intake therefore cannot truthfully assign a canonical proposition
or `H0` status.

## Candidate source work

Ronald Jensen's 1972 work on the fine structure of the constructible hierarchy is a historical
primary-source search anchor, not accepted evidence here. The later source audit must locate and
inspect an immutable edition and exact passage, record theorem/definition number and page, every
foundation and model assumption, the proof boundary and errata, and obtain independent review.
Authoritative modern texts may help disambiguate notation but cannot silently select a different
claim.

## Crosswalk

| Repository phrase | Mathematical choice still required | Required Lean component | Intake status |
|---|---|---|---|
| "diamond principle" | `Diamond(omega_1)`, generalized `Diamond(kappa)`, `Diamond(S)`, or a relative theorem | one concrete proposition and checked maps among any alternate encodings | absent |
| guessing sequence | subsets of each ordinal, functions, or coded objects | dependent sequence with stagewise restriction/type condition | definition open |
| "correctly guesses" | equality with target restriction at a stage | restriction/intersection operation and equality predicate | open |
| stationary often | selected club/stationary convention and ambient cardinal/model | predicates for club and stationary subsets | API and semantics open |
| Jensen, 1972 | attribution and likely constructible-universe boundary | encoded `L`, satisfaction, and internal cardinal/stationary notions if source requires them | source passage uninspected |
| `已验证` | untrusted inventory label | no Lean proposition or proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports ordinal aleph and topology support plus order boundedness. It checks the first
uncountable ordinal notation, ordinal initial segments, topological closedness, ordinal
closed-below, and order-theoretic unboundedness. These are nearby representation ingredients only.
A bounded case-insensitive search found no declaration named for diamond or stationary sets in
pinned mathlib's `Mathlib/SetTheory` tree; the only `club` hit was an informal TODO comment about
closed sets. This negative result is not the later immutable formal anchor audit and makes no claim
about all external Lean projects.
