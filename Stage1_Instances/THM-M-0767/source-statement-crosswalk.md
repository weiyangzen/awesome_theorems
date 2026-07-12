# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` records the Chinese title `康托尔定理`, attributes it to Georg
Cantor in 1891, and states `任何集合的幂集基数严格大于原集合` (the power set of every set has
strictly greater cardinality than the original set). Stage0 repeats this wording but leaves exact
definitions, hypotheses, proof route, dependencies, axioms, and formal artifacts open. The
manifest deliberately preserves `已验证` only as untrusted source metadata.

The repository wording identifies a stable theorem family and a strict-cardinality conclusion, but
it is not a pinpoint human-proof source. It does not specify a foundational set theory, cardinal
comparison convention, universe policy, or the relationship between its set-level wording and a
Lean type-level encoding.

## Primary-source candidate

The historical primary candidate is Georg Cantor, *Uber eine elementare Frage der
Mannigfaltigkeitslehre*, **Jahresbericht der Deutschen Mathematiker-Vereinigung** 1 (1891),
75-78. This bibliographic lead has not been verified against an immutable scan during intake; the
exact edition, pages containing the statement and proof, terminology, assumptions, translations,
later corrections, and errata remain open. It is therefore a discovery anchor, not `H0` evidence.
The source audit must inspect and hash a stable copy and obtain independent review.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "every set" | arbitrary `A`, including empty and finite cases | `alpha : Type u`, `s : Set alpha`, subtype cardinal | frozen and elaborated |
| "power set" | all subsets of `A` | subtype `Set.powerset s` | frozen and elaborated |
| "cardinality" | cardinal assigned to a type/set | `Cardinal.mk s` and `Cardinal.mk (Set.powerset s)` | frozen and elaborated |
| "strictly greater" | `|A| < |P(A)|` | strict order on `Cardinal`; checked normalization through `2 ^ Cardinal.mk s` | frozen and elaborated |
| diagonal argument | no map `A -> P(A)` is surjective | `Function.cantor_surjective` or an audited local derivation | supporting candidate only |
| singleton map | injection `A -> P(A)` | `a |-> {a}` and its injectivity | expected bridge; not yet frozen |
| Cantor / 1891 | historical provenance | no Lean proof credit | primary candidate uninspected |
| `已验证` | untrusted inventory label | no proposition or receipt | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
the types of `Function.cantor_surjective`, `Function.cantor_injective`, `Cardinal.mk_set`,
`Cardinal.mk_powerset`, and `Cardinal.cantor`. These declarations show that relevant encoding and
candidate theorem APIs are locally available. They do not establish exact source-statement
identity, accepted proof-body provenance, axiom closure, or `M0`; those belong to the statement and
anchor-audit phases.

Before `H0`, an independent reviewer must approve the immutable primary-source locator, exact
statement and assumptions, diagonal proof boundary, terminology/translation, corrections and
errata, and the row-by-row source-to-Lean map. Before machine credit, proof-body and anchor
provenance must pass the downstream audit. The chosen target's type-level and cardinal-exponential
alternate encodings are now related by checked Lean declarations in `Statement.lean`.
