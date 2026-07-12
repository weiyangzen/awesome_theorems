# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `方框原理`, attributes it to Ronald
Jensen, gives the year 1972, and describes it only as `组合集合论原理` ("combinatorial set-theory
principle"). Stage0 repeats those fields while leaving the exact definition, premises, proof,
equivalent formulations, axioms, and formal artifact open. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted`.

This is secondary inventory metadata, not a statement-bearing source. It gives no notation,
indexing cardinal, quantifiers, club/coherence clauses, conclusion, publication title, edition,
theorem number, page, errata, proof, or machine artifact. The adjacent diamond-principle entry does
not disambiguate square.

## Candidate source work

Jensen's original 1972 work is a historical locator supplied only indirectly by the repository
metadata; no publication or passage has been accepted at intake. The source audit must identify
and inspect an immutable primary publication or a precise authoritative edition. It must record
the definition/theorem and page, ambient model and foundation, every parameter and assumption,
proof boundary, and errata, followed by independent review. A modern source may clarify notation
but cannot silently replace the selected historical claim.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "square principle" | a coherent sequence of clubs | a family/function of ordinal-indexed sets and a coherence predicate | family identified; exact variant open |
| "club" | closed and unbounded subset of an ordinal | source-faithful predicates for closure and cofinality | encoding ingredients only |
| coherence | agreement at limit points | restriction/intersection equality with exact binder scope | clause and limit-point convention open |
| order-type bound | smallness of each club | ordinal order type or cardinal bound | strictness and bound open |
| width | one club or a small family at each index | singleton- or set-valued sequence | open |
| thread | a global club cohering with the sequence | quantified nonexistence predicate | primitive/derived/omitted status open |
| Jensen, 1972 | attribution and date | provenance record, not a Lean term | exact source anchor absent |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports cardinal cofinality and ordinal arithmetic and checks ordinal/cardinal/set APIs that
could support a later encoding. These are ingredients only. The probe does not define club,
coherence, a square sequence, or any square proposition, and the later anchor audit must conduct
the precommitted declaration search independently.
